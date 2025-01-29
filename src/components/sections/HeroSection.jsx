function HeroSection() {
  return (
    <div className="mt-12 bg-gradient-to-r from-[#fd8878]/50 to-[#ffd7c9] py-10 px-7 sm:py-20 sm:px-14">
      <h2 className="text-center text-2xl sm:text-3xl font-bold text-gray-800 mb-8">
        Your Gateway to the Latest in <br /> Tech Innovation
      </h2>
      <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-8">
        <button className="cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 focus-visible:ring-red-600 px-6 py-2 text-[#a32816] border border-[#a32816] rounded-lg hover:bg-red-800 hover:text-white transition duration-300">
          Login
        </button>
        <button className="cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-red-900 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 px-6 py-2 text-amber-50 bg-[#a32816] rounded-lg hover:bg-red-800 transition duration-300">
          Register
        </button>
      </div>
      <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
        <p className="italic text-gray-800">Never miss an update!</p>
        <button className="cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-red-900 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 px-6 py-2 bg-gradient-to-r from-[#a32816] to-[#ee6649] rounded-lg shadow-orange-500 text-amber-50 hover:from-red-800 hover:to-orange-500 hover:scale-105 transition duration-300">
          Subscribe to newsletter
        </button>
      </div>
    </div>
  );
}

export default HeroSection;
