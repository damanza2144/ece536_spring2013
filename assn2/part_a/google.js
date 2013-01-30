function initialize() {

	// Denver
	var myLatlngDenver = new google.maps.LatLng( 39.7178, -105.0161 );

	// Albuquerque
	var myLatlngAbq = new google.maps.LatLng( 35.0844909, -106.6511367 );

	// HOME - ABQ (RIO SENDA)
	var myLatlngRioSenda = new google.maps.LatLng( 35.0288, -106.7429 );

	// HOME - RIO CHAMA
	var myLatlngRioChama = new google.maps.LatLng( 36.1513, -106.1697 );

	// center location
	// denver - albuquerque / 2 = lat, long
	var myMidLatLong = new google.maps.LatLng( 37.5813545, -105.83361835 );

	var myOptionsGoogle = {
		zoom: 6,
		center: myLatlngRioChama,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}

	var mapGoogle = new google.maps.Map( document.getElementById( "map_canvas" ), myOptionsGoogle );

	var contentStringAbq = '<div id="content0">' +
					'<div id="abqContent">' +
					'<p><b>ECE536_DManzanares: </b></p>' +
					'<p>Albuquerque, New Mexico, USA ( Lat:35.0844909; Lng=-106.6511367)</p>' +
					'<p>This is the city where me and my family currently reside.</p>' +
					'</div>' +
					'</div>';

	var contentStringRioSenda = '<div id="content1">' +
					'<div id="riosendaContent">' +
					'<p><b>ECE536_DManzanares: </b></p>' +
					'<p>My House, USA ( Lat:35.0288; Lng=-106.7429)</p>' +
					'<p>This is the location where I reside.</p>' +
					'</div>' +
					'</div>';

	var contentStringRioChama = '<div id="content2">' +
					'<div id="riochamaContent">' +
					'<p><b>ECE536_DManzanares: </b></p>' +
					'<p>Rio Chama, New Mexico, USA ( Lat:36.1513; Lng=-106.1697)</p>' +
					'<p>This is the location where I call "home".</p>' +
					'</div>' +
					'</div>';

	var contentStringDenver = '<div id="content3">' +
					'<div id="denverContent">' +
					'<p><b>ECE536_DManzanares: </b></p>' +
					'<p>Denver, Colorado, USA ( Lat:39.7178; Lng=-105.0161 )</p>' +
					'<p>This is one of my favorite places to visit - Denver.</p>' +
					'</div>' +
					'</div>';

	var infowindowAbq = new google.maps.InfoWindow( { content: contentStringAbq } );
	var infowindowRioSenda = new google.maps.InfoWindow( { content: contentStringRioSenda } );
	var infowindowRioChama = new google.maps.InfoWindow( { content: contentStringRioChama } );
	var infowindowDenver = new google.maps.InfoWindow( { content: contentStringDenver } );

	var markerRioChama = new google.maps.Marker({
				position: myLatlngRioChama,
				map: mapGoogle,
				title: 'My Home - Rio Chama'
	});

	google.maps.event.addListener( markerRioChama, 'click', function() { infowindowRioChama.open( mapGoogle, markerRioChama ); });

	var myOptionsHybrid = {
			zoom: 6,
			center: myMidLatLong,
			mapTypeId: google.maps.MapTypeId.HYBRID
	}

	var mapHybrid = new google.maps.Map( document.getElementById( "map_canvas_hybrid" ), myOptionsHybrid );

	var markerHybridAbq = new google.maps.Marker({
				position: myLatlngAbq,
				map: mapHybrid,
				title: 'Albuquerque, NM'
	});

	var markerHybridRioSenda = new google.maps.Marker({
				position: myLatlngRioSenda,
				map: mapHybrid,
				title: 'My Home - Rio Senda'
	});

	var markerHybridRioChama = new google.maps.Marker({
				position: myLatlngRioChama,
				map: mapHybrid,
				title: 'My Home - Rio Chama'
	});

	var markerHybridDenver = new google.maps.Marker({
				position: myLatlngDenver,
				map: mapHybrid,
				title: 'My Favorite Place - Denver'
	});

	google.maps.event.addListener( markerHybridAbq, 'click', function() { infowindowAbq.open( mapHybrid, markerHybridAbq ); });
	google.maps.event.addListener( markerHybridRioSenda, 'click', function() { infowindowRioSenda.open( mapHybrid, markerHybridRioSenda ); });
	google.maps.event.addListener( markerHybridRioChama, 'click', function() { infowindowRioChama.open( mapHybrid, markerHybridRioChama ); });
	google.maps.event.addListener( markerHybridDenver, 'click', function() { infowindowDenver.open( mapHybrid, markerHybridDenver ); });
}
