const adList = [
    "https://www.youtube.com/embed/PT_ysnG1qkg",
    "https://www.youtube.com/embed/cZZ_5MOhWw0",
    "https://www.youtube.com/embed/W5XieFKuXlQ",
    "https://www.youtube.com/embed/Ii6Xgj3a-gQ",
    "https://www.youtube.com/embed/AucbTGClNTs",
    "https://www.youtube.com/embed/bkwl1u7uC3k",
    "https://www.youtube.com/embed/hzqoQJOoBC8",
    "https://www.youtube.com/embed/TxE4qmu6_QY",
    "https://www.youtube.com/embed/ARpnSZV3IY4",
    "https://www.youtube.com/embed/jOMCPTFTzcs",
    "https://www.youtube.com/embed/JJitmkV57DY",
    "https://www.youtube.com/embed/S0ZDpCzJEmI",
    "https://www.youtube.com/embed/PYhIKzLA-N8",
    "https://www.youtube.com/embed/GAiXqXvMuFY"
];

let adTimerInterval = null;
let adTimeLeft = 15;

function watchAd() {
    const modal = document.getElementById('ad-modal');
    const iframeHolder = document.getElementById('ad-iframe-holder');
    const timerElem = document.getElementById('ad-timer');
    const closeBtn = document.getElementById('ad-close-btn');

    const randomUrl = adList[Math.floor(Math.random() * adList.length)] + "?autoplay=1&controls=0&disablekb=1";

    iframeHolder.innerHTML = `<iframe width="100%" height="100%" src="${randomUrl}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
    
    modal.style.display = 'flex';
    closeBtn.style.display = 'none';
    adTimeLeft = 15;
    timerElem.innerText = `Ad Ends in ${adTimeLeft}s`;

    adTimerInterval = setInterval(() => {
        adTimeLeft--;
        if (adTimeLeft > 0) {
            timerElem.innerText = `Ad Ends in ${adTimeLeft}s`;
        } else {
            clearInterval(adTimerInterval);
            timerElem.innerText = "Ad Finished!";
            closeBtn.style.display = 'flex';
        }
    }, 1000);
}

function handleAdClick() {
    window.open('https://avelia.oneapp.dev', '_blank');
}

function finishAd() {
    const modal = document.getElementById('ad-modal');
    const iframeHolder = document.getElementById('ad-iframe-holder');
    
    iframeHolder.innerHTML = '';
    modal.style.display = 'none';
    
    if (typeof userData !== 'undefined') {
        userData.mkr += 0.20;
        localStorage.setItem('lumina_user', JSON.stringify(userData));
        if (typeof updateUI === 'function') {
            updateUI();
        }
    }
}
