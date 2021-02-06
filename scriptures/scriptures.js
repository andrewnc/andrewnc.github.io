/*jslint
    browser, long
*/

/*global
    console, map, google
*/

/*property
    Animation, DROP, LatLng, LatLngBounds, Marker, animation, books, classKey,
    content, createElement, exec, extend, firstChild, fitBounds, forEach,
    fullName, getAttribute, getElementById, getElementsByClassName, gridName,
    hash, href, id, init, innerHTML, insertBefore, label, lat, length, lng, map,
    maps, maxBookId, minBookId, nextSibling, numChapters, onHashChanged,
    onerror, onload, open, panTo, parentBookId, parentNode, parse, position,
    push, querySelectorAll, response, send, setMap, setZoom, showLocation,
    slice, split, status, title, tocName
*/


const Scriptures = (function() {
    "use strict";

    // Constants
    const BOTTOM_PADDING = "<br /><br />";
    const CLASS_BOOKS = "books";
    const CLASS_VOLUME = "volume";
    const CLASS_BUTTON = "btn";
    const CLASS_CHAPTER = "chapter";
    const DIV_SCRIPTURE_NAVIGATOR = "scripnav";
    const DIV_SCRIPTURES = "scriptures";
    const INDEX_FLAG = 11;
    const INDEX_LATITUDE = 3;
    const INDEX_LONGITUDE = 4;
    const INDEX_PLACENAME = 2;
    const LAT_LNG_PARSER = /\((.*),'(.*)',(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),'(.*)'\)/;
    const REQUEST_GET = "GET";
    const REQUEST_STATUS_OK = 200;
    const REQUEST_STATUS_ERROR = 400;
    const TAG_HEADER5 = "h5";

    // Private Variables
    let books;
    let gmMarkers = [];
    let volumes;

    // Private Method Declaration
    let addMarker;
    let ajax;
    let booksGrid;
    let booksGridContent;
    let bookChapterValid;
    let cacheBooks;
    let chaptersGrid;
    let chaptersGridContent;
    let clearMarkers;
    let encodedScriptureUrlParams;
    let getScripturesCallback;
    let getScripturesFailure;
    let htmlAnchor;
    let htmlDiv;
    let htmlElement;
    let htmlLink;
    let htmlHashLink;
    let navigateHome;
    let navigateBook;
    let navigateChapter;
    let nextChapter;
    let previousChapter;
    let setupMarkers;
    let titleForBookChapter;
    let volumesGridContent;

    // Public Method Declaration
    let init;
    let onHashChanged;
    let showLocation;


    // Private Methods
    addMarker = function(placeName, lat, lng){

        let isOnMap = false;
        gmMarkers.forEach(function(marker){
            if ((Number(lat) === marker.position.lat()) && (Number(lng) === marker.position.lng())){
                isOnMap = true;
            }
        });

        if (!isOnMap){
            let marker = new google.maps.Marker({
                position: {lat: Number(lat), lng: Number(lng)},
                map,
                title: placeName,
                label: placeName,
                animation: google.maps.Animation.DROP
            });

            gmMarkers.push(marker);
        }
    };

    ajax = function(url, successCallback, failCallback, skipJsonParse){
        let request = new XMLHttpRequest();

        request.open(REQUEST_GET, url, true);

        request.onload = function() {
        if (request.status >= REQUEST_STATUS_OK && request.status < REQUEST_STATUS_ERROR) {
            let data = (
                skipJsonParse
                ? request.response
                : JSON.parse(request.response)
            );

            if(typeof successCallback === "function"){
                successCallback(data);
            }
        } else {
            if(typeof failCallback === "function"){
                failCallback(request);
            }
        }
        };

        request.onerror = failCallback;
        request.send();
    };

    bookChapterValid = function (bookId, chapterId){
        let book = books[bookId];

        if (book === undefined || chapterId < 0 || chapterId > book.numChapters){
            return false;
        }

        if (chapterId === 0 && book.numChapters >0){
            return false;
        }

        return true;
    };

    booksGrid = function (volume) {
        return htmlDiv({
            classKey: CLASS_BOOKS,
            content: booksGridContent(volume)
        });
    };

    booksGridContent = function (volume) {
        let gridContent = "";

        volume.books.forEach(function (book){
            gridContent += htmlLink({
                classKey: CLASS_BUTTON,
                id: book.id,
                href: `#${volume.id}:${book.id}`,
                content: book.gridName
            });
        });

        return gridContent;
    };

    cacheBooks = function(callback){
        volumes.forEach(function (volume){
            let volumeBooks = [];
            let bookId = volume.minBookId;

            while(bookId <= volume.maxBookId){
                volumeBooks.push(books[bookId]);
                bookId += 1;
            }

            volume.books = volumeBooks;

        });

        if (typeof callback === "function"){
            callback();
        }
    };

    chaptersGrid = function(book){
        return htmlDiv({
            classKey: CLASS_VOLUME,
            content: htmlElement(TAG_HEADER5, book.fullName)
        }) + htmlDiv({
            classKey: CLASS_BOOKS,
            content: chaptersGridContent(book)
        });
    };

    chaptersGridContent = function(book){
        let gridContent = "";
        let chapter = 1;

        while(chapter <= book.numChapters){
            gridContent += htmlLink({
                classKey: `${CLASS_BUTTON} ${CLASS_CHAPTER}`,
                id: chapter,
                href: `#${book.parentBookId}:${book.id}:${chapter}`,
                content: chapter
            });
            chapter += 1;
        }

        return gridContent;
    };

    clearMarkers = function (){
        gmMarkers.forEach(function(marker){
            marker.setMap(null);
        });

        gmMarkers = [];
    };

    encodedScriptureUrlParams = function (bookId, chapterId, verses, isJst) {
        if (bookId !== undefined && chapterId !== undefined){
            let options = "";

            if (verses !== undefined){
                options += verses;
            }

            if (isJst !== undefined){
                options += "&jst=JST";
            }

            return `https:\/\/scriptures.byu.edu/mapscrip/mapgetscrip.php?book=${bookId}&chap=${chapterId}&verses${options}`;

        }
        // default to undefined return
    };

    getScripturesCallback = function(chapterHTML){
        document.getElementById(DIV_SCRIPTURES).innerHTML = chapterHTML;


        let ids = location.hash.slice(1).split(":").map((x) => Number(x));
        let bookId = ids[1];
        let chapterId = ids[2];
        let navHeading = document.getElementsByClassName("navheading")[0];
        let nextChapterInfo = nextChapter(bookId, chapterId);

        let prevChapterInfo = previousChapter(bookId, chapterId);

        if (nextChapterInfo !== undefined){
            let nextBookId = nextChapterInfo[0];
            let nextChapterId = nextChapterInfo[1];
            let nextAltTxt = nextChapterInfo[2];

            let navArrowNext = htmlLink({
                classKey: "nextArrow",
                content: "next",
                href: `#${books[nextBookId].parentBookId}:${nextBookId}:${nextChapterId}`
            });

            let templateNext = document.createElement("template");
            templateNext.innerHTML = navArrowNext;
            navHeading.parentNode.insertBefore(templateNext.content.firstChild, navHeading.nextSibling);
        }


        if (prevChapterInfo !== undefined){
            let prevBookId = prevChapterInfo[0];
            let prevChapterId = prevChapterInfo[1];
            let prevAltTxt = prevChapterInfo[2];

            let navArrowPrev = htmlLink({
                classKey: "prevArrow",
                content: "prev",
                href: `#${books[prevBookId].parentBookId}:${prevBookId}:${prevChapterId}`
            });

            let templatePrev = document.createElement("template");
            templatePrev.innerHTML = navArrowPrev;
            navHeading.parentNode.insertBefore(templatePrev.content.firstChild, navHeading.nextSibling);
        }
        setupMarkers();
    };

    getScripturesFailure = function(){
        document.getElementById(DIV_SCRIPTURES).innerHTML =
        htmlElement("p", "unable to retrieve chapter contents");
    };

    htmlAnchor = function (volume) {
        return `<a name="v${volume.id}" />`;
    };

    htmlDiv = function (parameters) {
        let classString = "";
        let contentString = "";
        let idString = "";

        if (parameters.classKey !== undefined){
            classString = ` class="${parameters.classKey}"`;
        }

        if (parameters.content !== undefined){
            contentString = parameters.content;
        }

        if (parameters.content !== undefined){
            idString = ` id="${parameters.id}"`;
        }

        return `<div${idString}${classString}>${contentString}</div>`;
    };

    htmlElement = function (tagName, content) {
        return `<${tagName}>${content}</${tagName}>`;
    };

    htmlLink = function (parameters) {
        let classString = "";
        let contentString = "";
        let hrefString = "";
        let idString = "";

        if (parameters.classKey !== undefined){
            classString = ` class="${parameters.classKey}"`;
        }

        if (parameters.content !== undefined){
            contentString = parameters.content;
        }

        if (parameters.href !== undefined){
            hrefString = ` href="${parameters.href}"`;
        }

        if (parameters.content !== undefined){
            idString = ` id="${parameters.id}"`;
        }

        return `<a${idString}${classString}${hrefString}>${contentString}</a>`;
    };

    htmlHashLink = function(hashArguments, content) {
        return `<a href="javascript:void(0)" onclick="changeHash(${hashArguments})">${content}</a>`;
    };


    navigateChapter = function(bookId, chapterId) {
        ajax(encodedScriptureUrlParams(bookId, chapterId),
        getScripturesCallback, getScripturesFailure, true);

    };

    navigateBook = function(bookId) {
        let book = books[bookId];

        if (book.numChapters <= 1){
            // clever code because numChapters also corresponds
            // to the chapter number itself we wish to display
            navigateChapter(bookId, book.numChapters);
        }else{
            document.getElementById(DIV_SCRIPTURES).innerHTML = htmlDiv({
                id: DIV_SCRIPTURE_NAVIGATOR,
                content: chaptersGrid(book)
            });

        }
    };

    navigateHome = function(volumeId) {
        document.getElementById(DIV_SCRIPTURES).innerHTML = htmlDiv({
            id: DIV_SCRIPTURE_NAVIGATOR,
            content: volumesGridContent(volumeId)
        });
    };

    nextChapter = function(bookId, chapterId){
        let book = books[bookId];

        if (book !== undefined){
            if (chapterId < book.numChapters){
                return [
                    bookId,
                    chapterId + 1,
                    titleForBookChapter(book, chapterId + 1)
                ];
            }

            let nextBook = books[bookId + 1];

            if (nextBook !== undefined){
                let nextChapterValue = 0;
                if (nextBook.numChapters  > 0){
                    nextChapterValue = 1;
                }
                return [
                    nextBook.id,
                    nextChapterValue,
                    titleForBookChapter(nextBook, nextChapterValue)
                ];
            }
        }
    };

    previousChapter = function(bookId, chapterId){
        let book = books[bookId];

        if (book !== undefined){
            if (chapterId > 1){
                return [
                    bookId,
                    chapterId - 1,
                    titleForBookChapter(book, chapterId - 1)
                ];
            }

            let prevBook = books[bookId - 1];

            if (prevBook !== undefined){
                return [
                    bookId - 1,
                    prevBook.numChapters,
                    titleForBookChapter(prevBook, prevBook.numChapters)
                ];
            }
        }

    };

    setupMarkers = function(){
        if (gmMarkers.length > 0){
            clearMarkers();
        }

        // TODO remove magic string for query selector
        document.querySelectorAll("a[onclick^=\"showLocation(\"]").forEach(function (element) {
            let matches = LAT_LNG_PARSER.exec(element.getAttribute("onclick"));

            if (matches){
                let placeName = matches[INDEX_PLACENAME];
                let latitude = matches[INDEX_LATITUDE];
                let longitude = matches[INDEX_LONGITUDE];
                let flag = matches[INDEX_FLAG];

                if (flag !== ""){
                    placeName = `${placeName} ${flag}`;
                }

                addMarker(placeName, latitude, longitude);
            }
        });

        let bounds = new google.maps.LatLngBounds();
        if(gmMarkers.length >= 0){
            gmMarkers.forEach(function (marker){
                bounds.extend({lat:marker.position.lat(), lng:marker.position.lng()});
            });
        } else {
            bounds.extend({lat: 31.7683, lng: 35.2137});
        }

        map.fitBounds(bounds);
    };

    titleForBookChapter = function(book, chapterId){
        if (book !== undefined){
            if(chapterId > 0){
                return `${book.tocName} ${chapterId}`;
            }

            return book.tocName;
        }
    };

    volumesGridContent = function (volumeId) {
        let gridContent = "";

        volumes.forEach(function (volume) {
            if (volumeId === undefined || volumeId === volume.id){
                gridContent += htmlDiv({
                    classKey: CLASS_VOLUME,
                    content: htmlAnchor(volume) + htmlElement(TAG_HEADER5, volume.fullName),
                    id: volumeId
                });

                gridContent += booksGrid(volume);
            }
        });

        return gridContent + BOTTOM_PADDING;
    };

    // Public Methods
    init = function(callback) {
        let booksLoaded = false;
        let volumesLoaded = false;

        ajax("https://scriptures.byu.edu/mapscrip/model/books.php",
              function (data) {
                  books = data;
                  booksLoaded = true;

                  if (volumesLoaded) {
                      cacheBooks(callback);
                  }
              });
        ajax("https://scriptures.byu.edu/mapscrip/model/volumes.php",
              function (data) {
                  volumes = data;
                  volumesLoaded = true;

                  if(booksLoaded){
                      cacheBooks(callback);
                  }
              });

    };

    onHashChanged = function() {
        let ids = [];
        if (location.hash !== "" && location.hash.length > 1){
            ids = location.hash.slice(1).split(":").map((x) => Number(x));
        }

        if (ids.length <= 0) {
            navigateHome();
        } else if (ids.length === 1){
            let volumeId = ids[0];

            if (volumeId < volumes[0].id || volumeId > volumes.slice(-1)[0].id){
                navigateHome();
            } else {
                navigateHome(volumeId);
            }

        } else {
            let bookId = ids[1];

            if(books[bookId] === undefined){
                navigateHome();
            } else {
                if (ids.length === 2){
                    navigateBook(bookId);
                } else {
                    let chapterId = ids[2];
                    if(bookChapterValid(bookId, chapterId)){
                        navigateChapter(bookId, chapterId);
                    } else {
                        navigateHome();
                    }

                }
            }
        }
    };

    showLocation = function(geotagId, placename, latitude, longitude, viewLatitude, viewLongitude, viewTilt, viewRoll, viewAltitude, viewHeading){
        let center = new google.maps.LatLng(latitude, longitude);
        map.panTo(center);
        map.setZoom(viewAltitude);
    };

    return{
        init,
        onHashChanged,
        showLocation
    };
}());