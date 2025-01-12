const config = {
        API_BASE_URL: 'http://localhost:8000',
        getApiUrl: function(endpoint) {
                // 쿼리 파라미터가 있는지 확인
                const [path, query] = endpoint.split('?');
                // 기본 경로에만 trailing slash 추가
                const normalizedPath = path.endsWith('/') ? path : `${path}/`;
                // 쿼리 파라미터가 있으면 다시 붙임
                return `${this.API_BASE_URL}${normalizedPath}${query ? `?${query}` : ''}`;
    }
};

// 개발/운영 환경에 따라 BASE_URL을 동적으로 설정
const hostname = window.location.hostname;
if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    config.API_BASE_URL = 'https://bitbox-production.up.railway.app'; // trailing slash 제거
}