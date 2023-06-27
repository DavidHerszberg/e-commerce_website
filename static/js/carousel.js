let carousel = document.querySelector(".carousel");
let items = document.querySelectorAll(".carousel .carousel-item");

let prev = document.querySelector(".home-banner-top-arrow.prev"),
    next = document.querySelector(".home-banner-top-arrow.next");

startCarousel(carousel, items, prev, next);

function startCarousel(carousel, items, prev, next) {
    var posX1 = 0,
        posX2 = 0,
        posInitial,
        posFinal,
        threshold = 100,
        slides = items,
        slidesLength = slides.length,
        firstSlide = slides[0],
        lastSlide = slides[slidesLength - 1],
        cloneFirst = firstSlide.cloneNode(true),
        cloneLast = lastSlide.cloneNode(true),
        index = 0,
        allowShift = true;

    carousel.insertBefore(cloneLast, firstSlide);
    carousel.appendChild(cloneFirst);

    // Mouse drag event
    carousel.onmousedown = dragStart;

    // Touch events
    carousel.addEventListener('touchstart', dragStart);
    carousel.addEventListener('touchend', dragEnd);
    carousel.addEventListener('touchmove', dragAction);

    // Click events
    prev.addEventListener('click', function () { shiftSlide(1) });
    next.addEventListener('click', function () { shiftSlide(-1) });

    // Transition events
    carousel.addEventListener('transitionend', checkIndex);

    window.addEventListener('resize', fitToResize);

    fitToResize()

    function dragStart (e) {
        e = e || window.event;
        e.preventDefault();
        posInitial = carousel.offsetLeft;
        
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
        carousel.style.left = (carousel.offsetLeft - posX2) + "px";
      }

      function dragEnd (e) {
        carousel.classList.add('shifting');
        posFinal = carousel.offsetLeft;
        if (posFinal - posInitial < -(window.innerWidth / 3)) {
          shiftSlide(1, 'drag');
        } else if (posFinal - posInitial > (window.innerWidth / 3)) {
          shiftSlide(-1, 'drag');
        } else {
          carousel.style.left = (posInitial) + "px";
        }
    
        document.onmouseup = null;
        document.onmousemove = null;
      }

      function shiftSlide(dir, action) {
        carousel.classList.add('shifting');
        
        if (allowShift) {
          if (!action) { posInitial = carousel.offsetLeft; }
    
          if (dir == 1) {
            carousel.style.left = (posInitial - window.innerWidth) + "px";
            index--;      
          } else if (dir == -1) {
            carousel.style.left = (posInitial + window.innerWidth) + "px";
            index++;      
          }
        };     
        allowShift = false;
      }
      
      function checkIndex (){
        carousel.classList.remove('shifting');
    
        if (index == -1) {
          carousel.style.left = (slidesLength * window.innerWidth) + "px";
          index = slidesLength - 1;
        }
    
        if (index == slidesLength) {
          carousel.style.left = (1 * window.innerWidth) + "px";
          index = 0;
        }
        
        allowShift = true;
      }

      function fitToResize(){
        carousel.style.left = ((index + 1) * window.innerWidth) + "px";
      }
}