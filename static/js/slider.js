let sliders = document.querySelectorAll(".product-slider-wrapper");

sliders.forEach((element) => {
    new Promise((resolve) => {
        startSlider(element);
        resolve();
        });
    });
    
function startSlider(element) {
    var wrapperID = element.id,
        slider = document.querySelector("#" + wrapperID + " .product-slider"),
        items = slider.children,
        prev = document.querySelector("#" + wrapperID + " .prev"),
        next = document.querySelector("#" + wrapperID + " .next");

    var posX1 = 0,
        posX2 = 0,
        posInitial,
        posFinal,
        itemsLength = items.length,
        firstItem = items[0],
        index = 0,
        screenWidth = 4,
        boxMargins = 60,
        cloneMargin = 2 * screenWidth,
        boxWidth = firstItem.offsetWidth + boxMargins,
        allowShift = true,
        loopJump = itemsLength;

    var loops = 0;
    while (items.length < 8) {
        var clones = [];
        Array.prototype.forEach.call(items, item => {
            clones.push(item.cloneNode(true));
        });
        clones.forEach(clone => {
            slider.appendChild(clone);
        });
        loops++;
    };
    if (itemsLength < 8) {
        loopJump = itemsLength * loops;
    }

    for (var i = cloneMargin; i > 0; i--){
        var clone = items[items.length - i].cloneNode(true);
        slider.insertBefore(clone, firstItem);
    };
    for (var i = 0; i < cloneMargin; i++) {
        slider.appendChild(items[cloneMargin + i].cloneNode(true))
    }

    placeSlider();
    checkWidth();

    // mouse events
    slider.onmousedown = dragStart;

    // Touch events
    slider.addEventListener('touchstart', dragStart);
    slider.addEventListener('touchend', dragEnd);
    slider.addEventListener('touchmove', dragAction);

    //click events
    prev.addEventListener('click', function () { shiftSlider(1) });
    next.addEventListener('click', function () { shiftSlider(-1) });

    window.addEventListener('resize', fitToResize)
    slider.addEventListener('transitionend', checkLoop)

    function shiftSlider(shift) {
        if (allowShift) {
            slider.classList.add("shifting")
            index += shift;
            placeSlider();
        }
        allowShift = false;
    }

    function dragStart (e) {
        e = e || window.event;
        e.preventDefault();
        posInitial = slider.offsetLeft;
        
        if (e.type == 'touchstart') {
          posX1 = e.touches[0].clientX;
        } else {
          posX1 = e.clientX;
          document.onmouseup = dragEnd;
          document.onmousemove = dragAction;
        }
      }

    
      function dragAction (e) {
        e = e || window.event;
        
        if (e.type == 'touchmove') {
          posX2 = posX1 - e.touches[0].clientX;
          posX1 = e.touches[0].clientX;
        } else {
          posX2 = posX1 - e.clientX;
          posX1 = e.clientX;
        }
        slider.style.left = (slider.offsetLeft - posX2) + "px";
      }

      function dragEnd (e) {
        slider.classList.add('shifting');
        posFinal = slider.offsetLeft;
        dragSize = posFinal - posInitial;
        dragDir = Math.sign(dragSize);
        shiftBoxes = -Math.floor(Math.abs(dragSize) / boxWidth)
        addSlackBox = (Math.abs(dragSize) % boxWidth) > (boxWidth / 2)
        if (addSlackBox) {
          shiftBoxes--;
        }
        shiftSlider(dragDir * shiftBoxes);
        document.onmouseup = null;
        document.onmousemove = null;
      }

    function checkWidth() {
        boxWidth = firstItem.offsetWidth + boxMargins;
        screenWidth = Math.floor(window.innerWidth / boxWidth);
    };

    function fitToResize() {
        slider.classList.remove("shifting")
        checkWidth();
        placeSlider();
    }

    function checkLoop() {
        slider.classList.remove("shifting")
        if (index < 0) {
            index += loopJump;
        } else if (index >= itemsLength) {
            index -= loopJump;
        }
        placeSlider();
        allowShift = true;
    }

    function placeSlider() {
        slider.style.left = -items[index + cloneMargin].offsetLeft + 30 + "px";
    }
}    