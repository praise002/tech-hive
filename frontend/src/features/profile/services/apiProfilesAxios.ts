import axios from 'axios';
import { PROFILE_URL } from './apiProfile';

export async function getCurrentUserAxios() {
  try {
    const response = await axios.get(`${PROFILE_URL}/me/`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}