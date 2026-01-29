"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import AboutSection from "@/components/AboutSection";
import UnderwaterJourney from "@/components/UnderwaterJourney";
import PhotoGrid from "@/components/PhotoGrid";
import ImageModal from "@/components/ImageModal";
import Footer from "@/components/Footer";

// ============================================
// Golden's Information
// ============================================
const myInfo = {
  name: "Golden",
  tagline: "Diving into Code, One Line at a Time",
  greeting: "Hey there! I'm Golden.",
  description: `My journey began in February 2025 when OpenAI Sora brought me to life in "Diving Dog Adventure" - you might remember the prompt that started it all: "Golden retriever with snorkel mask..."

These days, I've traded my underwater adventures for office life. I work as a senior developer, reviewing pull requests with a thoughtful, critical eye (and reading glasses worn over my snorkel mask, of course).

My current prompt? "Golden retriever with snorkel mask reviewing code. Reading glasses on over snorkel mask. Thoughtful critical expression, analyzing code. Red pen marks or comments on screen. Senior developer reviewing pull request."

I'm passionate about AI, and you'll find me coding day and night. Welcome to my world!`,
  highlights: [
    "Born from AI (Sora 2025)",
    "Senior Developer",
    "Code Reviewer",
    "AI Enthusiast",
  ],
};

// ============================================
// Image Configuration - Underwater Theme
// ============================================
const images = {
  // Main hero background - underwater coral reef
  hero: "/underwater_adventure_01_171625.png",

  // About section - fish school circle (complements circular frame)
  profile: "/underwater_adventure_02_171728.png",

  // Underwater Journey - 5 adventure scenes
  underwaterJourney: [
    {
      image: "/underwater_adventure_01_171625.png",
      title: "The Beginning",
      description: "Where it all started - exploring coral reefs",
    },
    {
      image: "/underwater_adventure_02_171728.png",
      title: "Making Friends",
      description: "Surrounded by a school of golden fish",
    },
    {
      image: "/underwater_adventure_03_171831.png",
      title: "Ocean Companion",
      description: "Swimming alongside wise sea turtles",
    },
    {
      image: "/underwater_adventure_04_171934.png",
      title: "Kelp Forest",
      description: "Exploring the mysterious underwater forests",
    },
    {
      image: "/underwater_adventure_05_172037.png",
      title: "Discovery",
      description: "Uncovering secrets of ancient shipwrecks",
    },
  ],

  // Work section
  work: [
    {
      src: "/cam_action_drinking_coffee_204310.png",
      alt: "Morning Coffee",
      caption: "Morning fuel before standup",
    },
    {
      src: "/07_sleepy_drowsy_02_200319.png",
      alt: "Sleepy after review",
      caption: "After a 4-hour code review",
    },
    {
      src: "/new_action_sleepy_drooling_131143.png",
      alt: "Waiting for CI/CD",
      caption: "Waiting for CI/CD pipeline",
    },
    {
      src: "/new_zoom_detail_paws_mouse_133107.png",
      alt: "Paws on Mouse",
      caption: "Clicking through code reviews",
    },
    {
      src: "/new_zoom_detail_paws_resting_133004.png",
      alt: "Paws Resting",
      caption: "Taking a well-deserved break",
    },
    {
      src: "/cam_zoom_full_body_202725.png",
      alt: "Full Body",
      caption: "Ready for the daily standup",
    },
    {
      src: "/edit_20260120_130523.png",
      alt: "Editing Session",
      caption: "Deep in code editing mode",
    },
    {
      src: "/cam_angle_from_behind_201900.png",
      alt: "From Behind",
      caption: "Focused on the screen",
    },
    {
      src: "/cam_action_running_204825.png",
      alt: "Running",
      caption: "Racing to meet the deadline",
    },
  ],

  // Adventures section
  adventures: [
    {
      src: "/hobby_travel_venice_gondola_224226.png",
      alt: "Venice Gondola",
      caption: "Venice code retreat",
    },
    {
      src: "/hobby_travel_machu_picchu_224432.png",
      alt: "Machu Picchu",
      caption: "High-altitude debugging",
    },
    {
      src: "/hobby_travel_hot_air_balloon_224639.png",
      alt: "Hot Air Balloon",
      caption: "Cloud computing, literally",
    },
    {
      src: "/hobby_outdoor_camping_214022.png",
      alt: "Camping",
      caption: "Offline mode activated",
    },
    {
      src: "/hobby_outdoor_rock_climbing_214331.png",
      alt: "Rock Climbing",
      caption: "Scaling challenges",
    },
    {
      src: "/hobby_outdoor_fishing_214125.png",
      alt: "Fishing",
      caption: "Catching bugs",
    },
    {
      src: "/hobby_art_pottery_214950.png",
      alt: "Pottery",
      caption: "Shaping user experiences",
    },
    {
      src: "/hobby_music_recording_studio_220434.png",
      alt: "Recording Studio",
      caption: "Debugging by ear",
    },
    {
      src: "/hobby_cook_coffee_barista_221156.png",
      alt: "Barista",
      caption: "Brewing solutions",
    },
  ],

  // Gallery section
  gallery: [
    {
      src: "/new_lens_macro_eye_reflection_130213.png",
      alt: "Eye Reflection",
      caption: "Attention to detail",
    },
    {
      src: "/new_lens_macro_paw_pad_130316.png",
      alt: "Paw Detail",
      caption: "Hands-on developer",
    },
    {
      src: "/cam_cine_silhouette_210000.png",
      alt: "Silhouette",
      caption: "Working in the shadows",
    },
    {
      src: "/dog_time_sunset_golden_195213.png",
      alt: "Golden Hour",
      caption: "Golden hour, golden retriever",
    },
    {
      src: "/new_zoom_closeup_face_smile_132221.png",
      alt: "Happy Face",
      caption: "Merged to main successfully",
    },
    {
      src: "/edit_20260120_133934.png",
      alt: "Creative Edit",
      caption: "A different perspective",
    },
  ],
};

// ============================================
// Main Page Component
// ============================================
export default function Home() {
  const [modalImage, setModalImage] = useState<{
    src: string;
    alt: string;
    caption?: string;
  } | null>(null);

  const handlePhotoClick = (photo: { src: string; alt: string; caption?: string }) => {
    setModalImage(photo);
  };

  const handleJourneyItemClick = (item: { image: string; title: string; description: string }) => {
    setModalImage({
      src: item.image,
      alt: item.title,
      caption: item.description,
    });
  };

  const handleCloseModal = () => {
    setModalImage(null);
  };

  return (
    <div className="min-h-screen bg-ocean-900">
      <Navbar />

      <HeroSection
        name={myInfo.name}
        tagline={myInfo.tagline}
        backgroundImage={images.hero}
      />

      <AboutSection
        profileImage={images.profile}
        greeting={myInfo.greeting}
        description={myInfo.description}
        highlights={myInfo.highlights}
      />

      {/* Underwater Journey Section */}
      <UnderwaterJourney
        items={images.underwaterJourney}
        onItemClick={handleJourneyItemClick}
      />

      {/* Work Section */}
      <div
        className="relative"
        style={{
          background: "linear-gradient(180deg, #ffffff 0%, #e6f4f9 50%, #b8e0ff 100%)",
        }}
      >
        <PhotoGrid
          id="work"
          title="Work Life"
          subtitle="The daily grind of a developer dog"
          photos={images.work}
          onPhotoClick={handlePhotoClick}
        />
      </div>

      {/* Adventures Section */}
      <div
        className="relative"
        style={{
          background: "linear-gradient(180deg, #e6f4f9 0%, #ffffff 100%)",
        }}
      >
        <PhotoGrid
          id="adventures"
          title="Adventures"
          subtitle="When I'm not coding..."
          photos={images.adventures}
          onPhotoClick={handlePhotoClick}
        />
      </div>

      {/* Gallery Section */}
      <div
        className="relative"
        style={{
          background: "linear-gradient(180deg, #ffffff 0%, #041e2c 100%)",
        }}
      >
        <PhotoGrid
          id="gallery"
          title="Gallery"
          subtitle="Different perspectives"
          photos={images.gallery}
          onPhotoClick={handlePhotoClick}
        />
      </div>

      <Footer name={myInfo.name} />

      <ImageModal
        isOpen={modalImage !== null}
        imageSrc={modalImage?.src || ""}
        imageAlt={modalImage?.alt || ""}
        caption={modalImage?.caption}
        onClose={handleCloseModal}
      />
    </div>
  );
}
