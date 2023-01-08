/**********
 * HEADER *
 **********/
// Header navbar
document.querySelectorAll(".header a").forEach((item) => {
    item.style.textDecoration = "none";
    item.style.color = "$text-color";
});

// Barrin's Banner
document.querySelectorAll('div.barrins-codex-banner').forEach((banner) => {
    // Banner style
    banner.style.position = "relative";
    banner.style.textAlign = "center";
    banner.style.color = "black";
    banner.classList.add("col-12");

    // Barrin's image
    var barrin = document.createElement("img");
    barrin.alt = "Bannière";
    barrin.style.width = "100%";
    barrin.style.objectFit = "cover";
    barrin.style.objectPosition = "50% 15%";
    barrin.lockedHeight = 0;

    var img_src = banner.querySelector("div.barrins-codex-banner-img");
    if (img_src && (img_src.innerText != "")) {
        barrin.src = img_src.innerText;
        img_src.remove();
    } else {
        barrin.src = "https://barrins-codex.org/static/img/banner.jpg";
    }

    // Title
    var title = document.createElement("div");
    var h1 = document.createElement("h1");
    title.style.position = "absolute";
    title.style.top = "50%";
    title.style.left = "50%";
    title.style.transform = "translate(-50%, -50%)";
    title.classList.add("fs-1");
    title.classList.add("text-capitalize");
    title.append(h1);
    if (banner.innerText != "") {
        h1.innerHTML = banner.innerHTML;
        banner.innerHTML = "";
        // Adaptating banner's height and opacity
        barrin.classList.add("opacity-75");
        barrin.style.height = "276px";
    }
    if ((banner.innerText != "") || !(img_src && (img_src.innerText != ""))) {
        barrin.style.height = "276px";
    }

    // Insert elements to DOM
    banner.append(barrin);
    banner.append(title);
});

// Add downsizing for bigger banner when scrolling down
window.addEventListener("scroll", event => {
    if (window.matchMedia("(min-width: 600px)").matches) { // Not on phones
        if (window.scrollY >= 276/3) {
            document.querySelectorAll('div.barrins-codex-banner img').forEach((banner) => {
                if (!banner.lockedHeight && banner.offsetHeight != 276) {
                    banner.previousHeight = banner.offsetHeight;
                    banner.lockedHeight = 1;
                    banner.style.transition = 'all .6s ease-in-out';
                    banner.style.width = "100%";
                    banner.style.objectFit = "cover";
                    banner.style.objectPosition = banner.style.objectPosition || "50% 40%";
                    banner.style.height = "276px";
                }
            });
        } else if (window.scrollY <= 276/2) {
            document.querySelectorAll('div.barrins-codex-banner img').forEach((banner) => {
                banner.style.height = banner.previousHeight + "px";
                banner.lockedHeight = 0;
                banner.style.transition = 'all .6s ease-in-out';
            });
        }
    }
});


/**********
 *  BODY  *
 **********/
// Body style
document.body.style.backgroundColor = "#e3e7e9";
document.body.style.display = "flex";
document.body.style.flexDirection = "column";
// Footer to bottom of page if not enough content
document.body.style.minHeight = "100vh";

// Section headers
document.querySelectorAll(".bg-header").forEach((item) => {
    item.style.backgroundColor = "#99A5C5";
});

// Article style
document.querySelectorAll("article").forEach((article) => {
    article.classList.add("col-8");
    article.classList.add("mx-auto");
    article.classList.add("my-4");
    article.style.flex = 1;
});

// Responsive img size in articles
document.querySelectorAll("li img").forEach((img) => {
    img.classList.add("col-12");
});

// Card display
// Only solution is to create a new style tag to operate the styling properly
// It may be due to a conflict with the tippy/popper instance
var css = `.card-name {
    color: #C05746 !important;
}
.card-image {
    padding: 0;
    outline: 0;
    max-width: 250px;
}`;
var head = document.head || document.getElementsByTagName('head')[0];
var style = document.createElement('style');
head.appendChild(style);

if (style.styleSheet){
  // This is required for IE8 and below.
  style.styleSheet.cssText = css;
} else {
  style.appendChild(document.createTextNode(css));
}

// Clear style
document.querySelectorAll(".clear").forEach((item) => {
    item.style.margin = "1.5em";
    item.style.padding = "0.5em 2em";
    item.style.borderRadius = "1em";
    item.style.clear = "both";
});

// Tip section
document.querySelectorAll("div.barrins-codex-tip").forEach((tip) => {
    // div.tip style
    tip.style.margin = "1.5em";
    tip.style.padding = "0.5em 2em";
    tip.style.borderRadius = "1em";
    tip.style.clear = "both";
    tip.style.backgroundColor = "#F7E3D1";
    tip.style.border = "1px solid #DC8C46";

    // Title
    var icon = document.createElement("span");
    icon.style.marginRight = "0.5em";
    icon.style.fontSize = "1.5em";
    icon.style.fontFamily = "FontAwesome";
    icon.style.fontWeight = "900";
    icon.innerHTML = "<i class=\"fa-solid fa-lightbulb\"></i>";
    tip.querySelectorAll("h3").forEach((title) => {
        title.style.color = "#583410";
        // Extract text content
        var text = document.createElement("span");
        text.innerHTML = title.innerHTML;
        title.innerHTML = "";
        // Create title
        title.append(icon);
        title.append(text);
    });
});

/**********
 * FOOTER *
 **********/
document.querySelectorAll("footer").forEach((foot) => {
    // Footer style
    foot.style.backgroundColor = "var(--color-white)";
    foot.style.marginTop = "auto";
    foot.style.marginBottom = "0";
    foot.style.fontSize = "0.9em";
    foot.style.textAlign = "center";
    foot.style.display = "flex";
    foot.style.flexDirection = "row";
    foot.style.justifyContent = "space-around";
    foot.style.clear = "both";

    // Link style
    foot.querySelectorAll("a").forEach((a) => {
        a.style.textDecoration = "none";
    });

    // Text style
    foot.querySelectorAll("p").forEach((p) => {
        p.style.fontSize = "0.8em";
        p.style.fontStyle = "italic";
        p.style.marginBottom = "0";
    });

    // Nav Style
    foot.querySelectorAll("nav").forEach((nav) => {
        // Icons
        var icon = document.createElement("span");
        icon.style.fontFamily = "FontAwesome";
        icon.style.fontWeight = "900";
        icon.style.padding = "0 0.5em";
        // Previous element
        nav.querySelectorAll(".prev").forEach((prev) => {
            // Clone icon
            var left = icon.cloneNode(true);
            left.innerHTML = "<i class=\"fa-solid fa-chevron-left\"></i>";
            // Text content
            var text = document.createElement("span");
            text.innerHTML = prev.innerHTML;
            prev.innerHTML = "";
            // Final rendering
            prev.append(left);
            prev.append(text);
        });
        // Next element
        nav.querySelectorAll(".next").forEach((next) => {
            // Clone icon
            var right = icon.cloneNode(true);
            right.innerHTML = "<i class=\"fa-solid fa-chevron-right\"></i>";
            // Final rendering
            next.append(right);
        });
        // Add empty containers
        var empty = document.createElement("a");
        // Check if .prev elt
        var prev = nav.querySelector(".prev");
        if (!prev) {
            prev = empty.cloneNode(true);
            prev.classList.add("prev");
            var content = nav.firstChild;
            nav.insertBefore(prev, content);
        }
        // Check if .next elt
        var next = nav.querySelector(".next");
        if (!next) {
            next = empty.cloneNode(true);
            next.classList.add("next");
            nav.append(next);
        }
        // Style
        nav.style.padding = "1em";
        nav.style.display = "flex";
        nav.style.justifyContent = "center";
        nav.querySelectorAll("a").forEach((a) => {
            a.classList.add("col-3");
        });
    });
});

