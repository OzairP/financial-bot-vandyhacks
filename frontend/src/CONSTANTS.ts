import axios from 'axios'

export const CONSTANTS = {
	endpoint: 'http://10.67.143.113:5000/',
	user_id: '5bde5ff33bdbba398b44289d',
	gkey: 'AIzaSyBgyZlcc1TdLlqORz4GibFMGU9d3EfLc64'
	//AIzaSyBCKYVKEdR5_xFmCHio3trHUOaE6a8WB5M
}

axios.defaults.baseURL = CONSTANTS.endpoint
