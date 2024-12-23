

function disable_button() {
    let button = document.getElementById("button_load_more");
    button.disabled = true;
    button.textContent = " End of the gallery ";
}

function on_response(request) {
    var response = JSON.parse(request.response);
    var gallery_main = document.getElementById('gallery_main');

    var list_images = response.more_images;

    if(list_images.length > 0){
        for(let j=0; j<list_images.length; j++) {
            var image = list_images[j];
            var newImage = $('<a class="gallery_thumb" href="'+image.image_original_url+'" data-sub-html=">"><img src="'+image.image_thumbnail_url+'" class="gallery_image"/></a>');
            newImage[0].dataset["subHtml"] = '<h2>'+image.title+'</h2><p>'+image.description+'</p><div class="licence">'+image.licence+'</div'
            newImage.appendTo(gallery_main);
        }
        gallery_main.dataset['last_id'] = response.last_id;
        gallery.refresh();
    }
    else{
        gallery_main.dataset['last_id'] = "-1";
        disable_button();
    }

    if(gallery_main.dataset['last_id'] == "-1") {
        disable_button();
    }

}

function request_more(last_id) {
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200)
            on_response(xhr);
    }
    xhr.open("GET", '/spirograph/load_more?max_id=' + last_id, true);
    xhr.send();
}

function click_load_more() {
    var gallery_main = document.getElementById('gallery_main');
    if(gallery_main.dataset['last_id'] >= 0){
        request_more(gallery_main.dataset['last_id']);
    }
    else {
        disable_button();
    }
}

let gallery_main = document.getElementById('gallery_main');
const gallery = lightGallery(gallery_main, {licenseKey: "D662B81C-D2E247E5-9EC0F4D2-F4B39655", plugins: [lgHash]});
