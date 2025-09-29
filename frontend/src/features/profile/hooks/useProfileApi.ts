import { ApiMethod, UpdateUserData } from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { useApi } from '../../auth/hooks/useApi';

export const useProfileApi = () => {
  const { sendRequest, sendAuthGuardedRequest } = useApi();

  const getCurrentUser = async (userIsNotAuthenticatedCallback: () => void) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.profile.me
    );

    return response.data;
  };

  const getCurrentUserProfile = async (
    userIsNotAuthenticatedCallback: () => void
  ) => {
    const currentUser = await getCurrentUser(userIsNotAuthenticatedCallback);
    const username = currentUser.data.username;
    const userProfile = routes.profile.byUsername(username);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      userProfile
    );

    return response.data;
  };

  const getUserProfileByUsername = async (username: string) => {
    const userProfile = routes.profile.byUsername(username);
    const response = await sendRequest(ApiMethod.GET, userProfile);

    return response.data;
  };

  const updateCurrentUserProfile = async (
    userIsNotAuthenticatedCallback: () => void,
    updateData: UpdateUserData
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.PATCH,
      routes.profile.me,
      updateData
    );

    return response.data;
  };

  const updateCurrentUserAvatar = async (
    userIsNotAuthenticatedCallback: () => void,
    formData: FormData
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.PATCH,
      routes.profile.avatar,
      formData
    );

    return response.data;
  };

  return {
    getCurrentUser,
    getCurrentUserProfile,
    getUserProfileByUsername,
    updateCurrentUserProfile,
    updateCurrentUserAvatar,
  };
};
