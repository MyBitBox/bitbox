const config = {
    API_BASE_URL: 'http://localhost:8000',
    getApiUrl: function(endpoint) {
        return `${this.API_BASE_URL}${endpoint}`;
    }
};

// 개발/운영 환경에 따라 BASE_URL을 동적으로 설정
const hostname = window.location.hostname;
if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    config.API_BASE_URL = 'https://bitbox-production.up.railway.app'; // 프로덕션 URL로 변경 필요
}