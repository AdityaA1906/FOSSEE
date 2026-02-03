import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auth API
export const authAPI = {
    signup: async (username, password, email = '', rememberMe = false) => {
        const response = await api.post('/auth/signup/', { username, password, email });
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));

            if (rememberMe) {
                localStorage.setItem('remembered_username', username);
                localStorage.setItem('remembered_password', btoa(password)); // Basic encoding
            }
        }
        return response.data;
    },

    login: async (username, password, rememberMe = false) => {
        const response = await api.post('/auth/login/', { username, password });
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));

            if (rememberMe) {
                localStorage.setItem('remembered_username', username);
                localStorage.setItem('remembered_password', btoa(password));
            } else {
                localStorage.removeItem('remembered_username');
                localStorage.removeItem('remembered_password');
            }
        }
        return response.data;
    },

    googleLogin: async (email) => {
        const response = await api.post('/auth/google/', { email });
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },

    getRememberedCredentials: () => {
        const username = localStorage.getItem('remembered_username');
        const password = localStorage.getItem('remembered_password');
        return username && password ? { username, password: atob(password) } : null;
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        // Keep remembered credentials for next login
    },

    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated: () => {
        const token = localStorage.getItem('access_token');
        return !!token && token.includes('.'); // Basic check for JWT format
    },
};

// Data API
export const dataAPI = {
    uploadCSV: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        // Use a clean post call, axios will set the boundary automatically
        const response = await api.post('/upload/', formData, {
            headers: {
                'Content-Type': undefined, // Force axios to auto-detect
            },
        });
        return response.data;
    },

    getEquipmentData: async (uploadId = null) => {
        const params = uploadId ? { upload_id: uploadId } : {};
        const response = await api.get('/data/', { params });
        return response.data;
    },

    getStatistics: async (uploadId = null) => {
        const params = uploadId ? { upload_id: uploadId } : {};
        const response = await api.get('/stats/', { params });
        return response.data;
    },

    getUploadHistory: async () => {
        const response = await api.get('/history/');
        return response.data;
    },

    generatePDF: async (datasetId = null) => {
        const response = await api.post('/generate-pdf/', { dataset_id: datasetId }, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default api;
