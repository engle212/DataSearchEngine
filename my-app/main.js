window.onload = init;

function init() {
  var mousePositionControl = new ol.control.MousePosition({
    // Define the coordinate format
    coordinateFormat: ol.coordinate.createStringXY(4), // Format the coordinates with 4 decimal places
    projection: 'EPSG:4326',
    target: document.getElementById('custom-mouse-position'),
    // Define the undefined HTML markup for coordinates outside the view extent
    undefinedHTML: '&nbsp;'
  })

  // Styles
  var fill = new ol.style.Fill({
		color: '#A7B1B7'
	});
	var stroke = new ol.style.Stroke({
		color: '#BA0C2F',
    width: 2
	});

	var circle = new ol.style.Circle({
		radius: 4,
		fill: fill,
		stroke: stroke
	});

	var vectorStyle = new ol.style.Style({
		fill: fill,
		stroke: stroke,
		image: circle
	});


  // Create a GeoJSON source
  var geojsonSource = new ol.source.Vector({
    url: 'http://localhost:8080/geoserver/searchengine/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=searchengine:dataframe&outputFormat=application/json',
    format: new ol.format.GeoJSON()
  });

  // Create a vector layer using the GeoJSON source
  var vectorLayer = new ol.layer.Vector({
    source: geojsonSource,
    style: vectorStyle
  });

  // Create a map instance
  var map = new ol.Map({
    target: 'map',
    renderer: 'canvas',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM({
          url: 'https://stamen-tiles.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png'
        }) // Use OpenStreetMap as the base layer
      }),
      vectorLayer
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([-83.0036617, 39.9867342]), // Set the initial center of the map
      zoom: 7 // Set the initial zoom level
    })
  });
  map.addControl(mousePositionControl);

  const selectedFill = new ol.style.Fill({
    color: '#A7B1B7',
  });

  const selectedStroke = new ol.style.Stroke({
    color: '#BA0C2F',
    width: 2,
  });
  const selectedStyle = new ol.style.Style({
    fill: selectedFill,
    stroke: selectedStroke,
    image: new ol.style.Circle({
      radius: 6,
		  fill: selectedFill,
		  stroke: selectedStroke
    })
  });

  // a normal select interaction to handle click
  const select = new ol.interaction.Select({
    style: function (feature) {
      const color = '#eeeeee';
      selectedStyle.getFill().setColor(color);
      return selectedStyle;
    },
  });
  map.addInteraction(select);

  const selectedFeatures = select.getFeatures();

  // a DragBox interaction used to select features by drawing boxes
  const dragBox = new ol.interaction.DragBox({
    condition: ol.events.condition.platformModifierKeyOnly,
  });

  map.addInteraction(dragBox);

  dragBox.on('boxend', function () {
    const boxExtent = dragBox.getGeometry().getExtent();
  
    // if the extent crosses the antimeridian process each world separately
    const worldExtent = map.getView().getProjection().getExtent();
    const worldWidth = ol.extent.getWidth(worldExtent);
    const startWorld = Math.floor((boxExtent[0] - worldExtent[0]) / worldWidth);
    const endWorld = Math.floor((boxExtent[2] - worldExtent[0]) / worldWidth);
  
    for (let world = startWorld; world <= endWorld; ++world) {
      const left = Math.max(boxExtent[0] - world * worldWidth, worldExtent[0]);
      const right = Math.min(boxExtent[2] - world * worldWidth, worldExtent[2]);
      const extent = [left, boxExtent[1], right, boxExtent[3]];
      const boxFeatures = vectorLayer.getSource()
        .getFeaturesInExtent(extent)
        .filter(
          (feature) =>
            !selectedFeatures.getArray().includes(feature) &&
            feature.getGeometry().intersectsExtent(extent)
        );
  
      // features that intersect the box geometry are added to the
      // collection of selected features
  
      // if the view is not obliquely rotated the box geometry and
      // its extent are equalivalent so intersecting features can
      // be added directly to the collection
      const rotation = map.getView().getRotation();
      const oblique = rotation % (Math.PI / 2) !== 0;
  
      // when the view is obliquely rotated the box extent will
      // exceed its geometry so both the box and the candidate
      // feature geometries are rotated around a common anchor
      // to confirm that, with the box geometry aligned with its
      // extent, the geometries intersect
      if (oblique) {
        const anchor = [0, 0];
        const geometry = dragBox.getGeometry().clone();
        geometry.translate(-world * worldWidth, 0);
        geometry.rotate(-rotation, anchor);
        const extent = geometry.getExtent();
        boxFeatures.forEach(function (feature) {
          const geometry = feature.getGeometry().clone();
          geometry.rotate(-rotation, anchor);
          if (geometry.intersectsExtent(extent)) {
            selectedFeatures.push(feature);
          }
        });
      } else {
        selectedFeatures.extend(boxFeatures);
      }
    }
  });
  
  // clear selection when drawing a new box and when clicking on the map
  dragBox.on('boxstart', function () {
    selectedFeatures.clear();
  });
  
  selectedFeatures.on(['add', 'remove'], function () {
    
    const headers = selectedFeatures.getArray().map((feature) => {
      return feature.getProperties();
    });

    let col = [];
    for (let i = 0; i < headers.length; i++) {
      for (let key in headers[i]) {
        if (col.indexOf(key) === -1) {
          col.push(key);
        }
      }
    }
    // Create table.
  const table = document.createElement("table");

  // Create table header row using the extracted headers above
  let tr = table.insertRow(-1);                   // table row

  for (let i = 0; i < col.length; i++) {
    let th = document.createElement("th");      // table header
    th.innerHTML = col[i];
    tr.appendChild(th);
  }

  // add json data to the table as rows.
  for (let i = 0; i < headers.length; i++) {

    tr = table.insertRow(-1);

    for (let j = 0; j < col.length; j++) {
      let tabCell = tr.insertCell(-1);
      tabCell.innerHTML = headers[i][col[j]];
    }
  }

  // Now, add the newly created table with json data, to a container.
  const divShowData = document.getElementById('showData');
  divShowData.innerHTML = "";
  divShowData.appendChild(table);
  });
  
  /////////////////////////////////////////////////////////////////
}
