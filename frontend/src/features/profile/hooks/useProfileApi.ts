import {
  ApiMethod,
  SaveArticleData,
  UpdateArticleData,
  UpdateUserData,
} from '../../../types/auth';
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

  const getUserArticles = async (
    userIsNotAuthenticatedCallback: () => void
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.profile.articles
    );

    return response.data;
  };

  const getUserArticleBySlug = async (
    userIsNotAuthenticatedCallback: () => void,
    slug: string
  ) => {
    const articleSlug = routes.profile.byArticle(slug);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      articleSlug
    );

    return response.data;
  };

  const updateUserArticleBySlug = async (
    userIsNotAuthenticatedCallback: () => void,
    slug: string,
    updateData: UpdateArticleData
  ) => {
    const articleSlug = routes.profile.byArticle(slug);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.PATCH,
      articleSlug,
      updateData
    );

    return response.data;
  };

  const getUserSavedArticles = async (
    userIsNotAuthenticatedCallback: () => void
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.profile.saved
    );

    return response.data;
  };

  const updateSavedArticle = async (
    userIsNotAuthenticatedCallback: () => void,
    updateData: SaveArticleData
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      routes.profile.saved,
      updateData
    );

    return response.data;
  };

  const getUserComments = async (
    userIsNotAuthenticatedCallback: () => void
  ) => {
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.profile.comments
    );

    return response.data;
  };

  return {
    getCurrentUser,
    getCurrentUserProfile,
    getUserProfileByUsername,
    getUserArticleBySlug,
    getUserSavedArticles,
    getUserComments,
    getUserArticles,
    updateCurrentUserProfile,
    updateCurrentUserAvatar,
    updateUserArticleBySlug,
    updateSavedArticle,
  };
};
