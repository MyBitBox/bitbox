// 로그인 상태 확인
function isLoggedIn() {
    return localStorage.getItem('token') !== null;
}

// 네비게이션 메뉴 업데이트
function updateNavigation() {
    const navLinks = document.querySelector('.nav-links');
    const currentPage = window.location.pathname.split('/').pop().split('.')[0];

    if (isLoggedIn()) {
        // 현재 페이지에 따라 다른 네비게이션 메뉴 표시
        let menuItems = [];

        if (currentPage !== 'dashboard') {
            menuItems.push(`<a href="/frontend/pages/dashboard.html" class="btn btn-outline">대시보드</a>`);
        }

        if (currentPage !== 'profile') {
            menuItems.push(`<a href="/frontend/pages/profile.html" class="btn btn-outline">프로필</a>`);
        }

        menuItems.push(`<button id="logoutBtn" class="btn btn-outline">로그아웃</button>`);

        navLinks.innerHTML = menuItems.join('');

        // 로그아웃 버튼에 이벤트 리스너 추가
        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('token');
            updateNavigation();
            // 현재 페이지가 보호된 페이지인 경우 메인 페이지로 리다이렉트
            const protectedPages = ['dashboard', 'profile'];
            if (protectedPages.includes(currentPage)) {
                window.location.href = '/frontend/index.html';
            }
        });
    } else {
        navLinks.innerHTML = `
            <a href="/frontend/pages/login.html" class="btn btn-outline">로그인</a>
            <a href="/frontend/pages/signup.html" class="btn btn-primary">회원가입</a>
        `;
    }
}

// auth.js에 추가
function checkProtectedPage() {
    const protectedPages = ['dashboard', 'profile'];
    const currentPage = window.location.pathname.split('/').pop().split('.')[0];

    if (protectedPages.includes(currentPage) && !isLoggedIn()) {
        window.location.href = '/frontend/pages/login.html';
    }
}

// 페이지 로드 시 네비게이션 초기화
document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
    checkProtectedPage();
});