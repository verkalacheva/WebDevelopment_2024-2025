function changeBackground() {
    document.body.style.backgroundColor = getRandomColor();
  }

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function toggleMusic() {
    const audio = document.getElementById('myAudio');
    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
}

function showVideo() {
    const video = document.getElementById('myVideo');
    const container = document.getElementById('videoContainer');
    container.style.display = 'block';
    video.currentTime = 0;
    video.play();

    video.onended = function() {
        container.style.display = 'none';
    };
}

function startStarfall() {
    for (let i = 0; i < 30; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.innerText = '⭐';

        star.style.left = Math.random() * 100 + 'vw';

        const duration = 3 + Math.random() * 2;
        star.style.animationDuration = duration + 's';

        document.body.appendChild(star);

        setTimeout(() => {
            star.remove();
        }, duration * 1000);
    }
}