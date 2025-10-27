import Rectangle from '../components/common/Rectangle';
import HeroSection from '../components/sections/HeroSection';
import Subscribe from '../components/sections/Subscribe';
import Articles from '../components/sections/Articles';
import ResourceSpotlight from '../components/sections/ResourceSpotlight';
import TechEvents from '../components/sections/TechEvents';
import TechJobs from '../components/sections/TechJobs';
import TechTool from '../components/sections/TechTool';
import TrendingArticles from '../components/sections/TrendingArticles';
// import { useAuthApi } from '../features/auth/hooks/useAuthApi';
// import { useEffect } from 'react';
// import { useGoogleSignup } from '../features/auth/hooks/useAuth';

function Home() {
  // const { login, fetchAuthRegisterUrl } = useAuthApi();
  // const email = 'ifeoluwapraise002@gmail.com';
  // const password = 'Esiveneta1964@';
  // const { fetchAuthRegisterUrl, isPending } = useGoogleSignup();

  // function handleClick(e) {
  //   e.preventDefault();
  //   fetchAuthRegisterUrl();
  // }

  // useEffect(() => {
  //   const testAuth = async () => {
  //     try {
  //       const result = await login({ email, password });
  //       console.log('Auth test result:', result);
  //       const result2 = await fetchAuthRegisterUrl();
  //       console.log('Auth test result 2:', result2);
  //     } catch (error) {
  //       console.error('Auth test error:', error);
  //     }
  //   };

  //   testAuth();
  // }, [login, fetchAuthRegisterUrl]);

  

  return (
    <div>
      <HeroSection />
      {/* <button onClick={handleClick} disabled={isPending}>
        {isPending ? 'Loading...' : 'Sign Up with Google'}
      </button> */}
      <TrendingArticles />
      <Articles />
      <TechJobs />
      <TechEvents />
      <TechTool />
      <ResourceSpotlight />
      <Rectangle />
      <Subscribe />
    </div>
  );
}

export default Home;
