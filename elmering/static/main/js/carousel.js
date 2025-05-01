// keydown listener
document.addEventListener('keydown', function (e) {
    if (e.code === 'Space') {
      e.preventDefault();
  
      // find .carousel-card only inside .carousel-item.active
      const activeCard = document.querySelector('.carousel-item.active .carousel-card');
      if (activeCard) {
        activeCard.classList.toggle('card-flipped');
      }
    }

    if (e.code === 'ArrowLeft' || e.code === 'KeyA') {
        e.preventDefault();
        const prevBtn = document.querySelector('.carousel-control-prev');
        if (prevBtn) prevBtn.click();
      }
      if (e.code === 'ArrowRight' || e.code === 'KeyD') {
        e.preventDefault();
        const nextBtn = document.querySelector('.carousel-control-next');
        if (nextBtn) nextBtn.click();
      }
});


// Mouse click handler
document.querySelectorAll('.carousel-card').forEach(card => {
    card.addEventListener('click', function() {
        this.classList.toggle('card-flipped');
    });
});


// Reset animation on slide change
document.getElementById('carouselExample').addEventListener('slid.bs.carousel', function() {
    document.querySelectorAll('.carousel-card').forEach(card => {
        card.classList.remove('card-flipped');
    });
});
