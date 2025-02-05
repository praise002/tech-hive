import Image from '../../components/common/Image';
import Tags from '../../components/common/Tags';
import Text from '../../components/common/Text';

function ArticleDetail() {
  return (
    <div>
      <Image
        alt="Article Image"
        src="/src/assets/articles/data-privacy-laws-to-watch-2025.png"
      />
      <div className="px-4 py-6 border border-[#889392]">
        <div className="mt-2 text-xs text-[#889392]">Posted 1 hour ago</div>
        <Text variant="h3" size="xl" bold={false} className="font-semibold">
          The Future of UI/UX: Trends to Watch in 2024
        </Text>
        <div>
          From AI-powered interfaces to immersive experiences, here are the key
          trends shaping UI/UX design and how designers can stay ahead designers
          must anticipate and adapt to these emerging trends. The rise of AI is
          poised to revolutionize user interactions, with chatbots, voice
          assistants, and personalized recommendations becoming increasingly
          prevalent. Designers will need to focus on creating intuitive and
          human-centered AI interactions, ensuring that these technologies
          enhance rather than hinder the user experience. Furthermore, Virtual
          Reality (VR), Augmented Reality (AR), and Mixed Reality (MR) are
          poised to redefine how we engage with digital content. Designers will
          need to explore new ways to create immersive and engaging user
          experiences in these emerging technologies. As data collection and
          analysis become more sophisticated, users will expect
          hyper-personalized experiences tailored to their individual needs and
          preferences. Designers will need to leverage data and AI to create
          truly personalized interfaces while maintaining user privacy and
          trust. Accessibility will continue to be a crucial consideration.
          Designers must ensure that their interfaces are usable by people with
          disabilities, including those with visual, auditory, motor, and
          cognitive impairments. Environmental sustainability will also become
          an increasingly important factor in design decisions. Designers will
          need to prioritize energy efficiency, reduce e-waste, and create
          interfaces that minimize their environmental impact. Lastly, the rise
          of no-code/low-code tools is empowering individuals and businesses to
          create digital experiences without extensive coding knowledge.
          Designers will need to adapt to this changing landscape and learn to
          collaborate effectively with citizen developers. By staying informed
          about these trends and adapting their skills accordingly, designers
          can ensure they remain at the forefront of the ever-evolving UI/UX
          landscape.
        </div>
        <Tags />
        <div className="flex justify-between">
          <img src="/src/assets/icons/reaction-light.png" alt="" />
          <img src="/src/assets/icons/Vector.png" alt="" />
        </div>
        <div>
          {/* Comments */}
          <Text variant="h4" size="lg" bold={false} className="font-semibold">
            Comments (1)
          </Text>
          {/* Chat */}
          <div>
            {/* New Chat */}
            <div>
              <img src="/src/assets/icons/iconamoon_profile-light.png" alt="" />
              <textarea
                placeholder="Add to discussion"
                name=""
                id=""
              ></textarea>
            </div>
            {/* User chat */}
            <div>
              <div>
                <img src="/src/assets/icons/Profile.png" alt="" />
              </div>
              <div>
                <p className="font-bold">
                  Adebayo Abibat <span className="ml-2">2h</span>
                </p>
                <p>This is really informative</p>
                <div>
                  <p>
                    <span>
                      <img src="/src/assets/icons/Like.png" alt="" />
                    </span>
                    Like
                  </p>
                  <p>
                    <span>
                      <img src="/src/assets/icons/Chat.png" alt="" />
                    </span>
                    Chat
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ArticleDetail;
