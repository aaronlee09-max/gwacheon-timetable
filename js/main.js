// 과천중앙고등학교 시간표 사이트 JS
function filterCards(containerId, searchTerm) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const cards = container.getElementsByClassName('card');
    const term = searchTerm.toLowerCase().trim();
    for (let card of cards) {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(term) ? '' : 'none';
    }
}

function setupSearch() {
    const teacherSearch = document.getElementById('teacher-search');
    if (teacherSearch) {
        teacherSearch.addEventListener('input', () => filterCards('teachers-grid', teacherSearch.value));
    }
    const classSearch = document.getElementById('class-search');
    if (classSearch) {
        classSearch.addEventListener('input', () => filterCards('classes-grid', classSearch.value));
    }
}

function addToRecent(name, url) {
    let recent = JSON.parse(localStorage.getItem('recentTimetables') || '[]');
    recent = recent.filter(item => item.name !== name);
    recent.unshift({ name, url, time: new Date().toISOString() });
    recent = recent.slice(0, 5);
    localStorage.setItem('recentTimetables', JSON.stringify(recent));
    renderRecent();
}

function renderRecent() {
    const container = document.getElementById('recent-list');
    if (!container) return;
    const recent = JSON.parse(localStorage.getItem('recentTimetables') || '[]');
    if (recent.length === 0) {
        container.innerHTML = '<p style="color:#64748b;">최근 조회한 시간표가 없습니다.</p>';
        return;
    }
    let html = '<div style="display:flex; flex-wrap:wrap; gap:10px;">'; 
    recent.forEach(item => {
        html += `<a href="${item.url}" class="btn" style="padding:8px 16px; font-size:0.9rem; background:#e0e7ff; color:#1e3a8a;">📋 ${item.name}</a>`;
    });
    html += '</div>';
    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
    setupSearch();
    renderRecent();
});