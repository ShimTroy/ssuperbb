// 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
var placeOverlay = new kakao.maps.CustomOverlay({zIndex: 1}),
    contentNode = document.createElement('div') // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다

var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(37.496374, 126.953504), // 지도의 중심좌표
        level: 2 // 지도의 확대 레벨
    };

// 지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

if (navigator.geolocation) {

    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(function (position) {

        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도

        var locPosition = new kakao.maps.LatLng(lat, lon)

        var imageSrc = '/static//brand/brand_logo_57x38.png', // 마커이미지의 주소입니다
            imageSize = new kakao.maps.Size(57, 38), // 마커이미지의 크기입니다
            imageOption = {offset: new kakao.maps.Point(19, 12)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

// 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption)

// 마커를 생성합니다
        var marker = new kakao.maps.Marker({
            position: locPosition,
            image: markerImage // 마커이미지 설정
        });
        marker.setMap(map);

        content = '<div style="padding: 5px; margin-bottom: 70px; margin-left: 15px;background: #ffc107; border: 1px solid #ffc107; border-radius: 5px; color: #ffffff; font-weight: 500; box-shadow: 1px 1px 2px 1px gray">내 위치</div>'

        var overlay = new kakao.maps.CustomOverlay({
            content: content,
            map: map,
            position: locPosition
        });

        map.setCenter(locPosition);
    });
}

// 커스텀 오버레이의 컨텐츠 노드에 css class를 추가합니다
contentNode.className = 'placeinfo_wrap';

// 커스텀 오버레이의 컨텐츠 노드에 mousedown, touchstart 이벤트가 발생했을때
// 지도 객체에 이벤트가 전달되지 않도록 이벤트 핸들러로 kakao.maps.event.preventMap 메소드를 등록합니다
addEventHandle(contentNode, 'mousedown', kakao.maps.event.preventMap);
addEventHandle(contentNode, 'touchstart', kakao.maps.event.preventMap);

// 커스텀 오버레이 컨텐츠를 설정합니다
placeOverlay.setContent(contentNode);

// 엘리먼트에 이벤트 핸들러를 등록하는 함수입니다
function addEventHandle(target, type, callback) {
    if (target.addEventListener) {
        target.addEventListener(type, callback);
    } else {
        target.attachEvent('on' + type, callback);
    }
}

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places(map);

// 카테고리로 은행을 검색합니다
ps.categorySearch('CS2', placesSearchCB, {useMapBounds: true});

// 키워드 검색 완료 시 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        for (var i = 0; i < data.length; i++) {
            displayMarker(data[i]);
        }
    }
}

// 지도에 마커를 표시하는 함수입니다
function displayMarker(place) {
    // 마커를 생성하고 지도에 표시합니다
    var marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x)
    });

    // 마커에 클릭이벤트를 등록합니다
    kakao.maps.event.addListener(marker, 'click', function () {
        var locPosition = new kakao.maps.LatLng(place.y, place.x)

        map.panTo(locPosition);
    });

    kakao.maps.event.addListener(marker, 'mouseover', function () {
        // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다

        var content = '<div class="placeinfo">' +
            '   <a class="title" href="' + place.place_url + '" target="_blank" title="' + place.place_name + '">' + place.place_name + '</a>';

        if (place.road_address_name) {
            content += '    <span title="' + place.road_address_name + '">' + place.road_address_name + '</span>' +
                '  <span class="jibun" title="' + place.address_name + '">(지번 : ' + place.address_name + ')</span>';
        } else {
            content += '    <span title="' + place.address_name + '">' + place.address_name + '</span>';
        }

        content += '    <span class="tel">' + place.phone + '</span>' +
            '</div>' +
            '<div class="after"></div>';

        contentNode.innerHTML = content;
        placeOverlay.setPosition(new kakao.maps.LatLng(place.y, place.x));
        placeOverlay.setMap(map);
    });
    kakao.maps.event.addListener(marker, 'mouseout', function () {
        contentNode.innerHTML = '';
        placeOverlay.setMap(map);
    });

}

kakao.maps.event.addListener(map, 'center_changed', function () {
    ps.categorySearch('CS2', placesSearchCB, {useMapBounds: true});
});
