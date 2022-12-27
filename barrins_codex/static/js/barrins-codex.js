/**********
 * HEADER *
 **********/
// Header navbar
document.querySelectorAll(".header a").forEach((item) => {
    item.style.textDecoration = "none";
    item.style.color = "$text-color";
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

// Card display
document.querySelectorAll(".card-name").forEach((item) => {
    item.style.color = "#C05746";
});
document.querySelectorAll(".card-image").forEach((item) => {
    item.style.padding = 0;
    item.style.outline = 0;
    item.style.maxWidth = "250px";
});

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

