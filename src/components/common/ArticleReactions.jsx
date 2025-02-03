function ArticleReactions() {
  return (
    <div className="flex flex-col">
      {/* Reactions and Bookmark Section */}
      <div className="flex justify-between items-center my-3">
        {/* Reactions */}
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1 text-lg">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full shadow-md">
              ❤️
            </span>
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full shadow-md -ml-2">
              😍
            </span>
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full shadow-md -ml-2">
              👍
            </span>
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full shadow-md -ml-2">
              🔥
            </span>
          </div>
          <div className="text-sm text-[#262A2A] font-medium">95 reactions</div>
        </div>

        {/* Bookmark */}
        <div className="flex items-center space-x-2">
          {/* Read Time */}
          <div className="text-sm text-[#262A2A]  font-medium">
            5 min read
          </div>
          <img
            src="/src/assets/icons/bookmark-light.png"
            alt="Bookmark"
            className="w-5 h-5"
          />
        </div>
      </div>

      {/* Posted Time */}
      <div className="text-xs text-[#889392]">Posted 1 hour ago</div>
    </div>
  );
}

export default ArticleReactions;
