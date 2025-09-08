import React, { useState } from 'react';
import { MediaFile } from '../types/product';

interface MediaGalleryProps {
  mediaFiles: MediaFile[];
}

const MediaGallery: React.FC<MediaGalleryProps> = ({ mediaFiles }) => {
  const [selectedMedia, setSelectedMedia] = useState<MediaFile | null>(null);

  if (!mediaFiles || mediaFiles.length === 0) {
    return null;
  }

  return (
    <>
      <div className="mt-3 grid grid-cols-2 gap-3 w-1/2">
        {mediaFiles.map((media, index) => (
          <div
            key={media.id}
            className="relative cursor-pointer hover:opacity-80 transition-opacity aspect-square"
            onClick={() => setSelectedMedia(media)}
          >
            {media.type === 'image' ? (
              <img
                src={`http://localhost:8000${media.thumbnail_url || media.url}`}
                alt={`Review media ${index + 1}`}
                className="w-full h-full object-cover rounded-lg"
              />
            ) : (
              <div className="relative w-full h-full">
                <video
                  src={`http://localhost:8000${media.url}`}
                  className="w-full h-full object-cover rounded-lg"
                  preload="metadata"
                />
                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-lg">
                  <div className="w-8 h-8 bg-white bg-opacity-80 rounded-full flex items-center justify-center">
                    ▶️
                  </div>
                </div>
              </div>
            )}
            
            <div className="absolute top-1 right-1 bg-black bg-opacity-50 text-white text-xs px-1 rounded">
              {media.type === 'video' ? '🎥' : '📷'}
            </div>
          </div>
        ))}
      </div>

      {/* Modal for full-size media */}
      {selectedMedia && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
          onClick={() => setSelectedMedia(null)}
        >
          <div className="max-w-4xl max-h-full p-4">
            {selectedMedia.type === 'image' ? (
              <img
                src={`http://localhost:8000${selectedMedia.url}`}
                alt="Full size"
                className="max-w-full max-h-full object-contain"
              />
            ) : (
              <video
                src={`http://localhost:8000${selectedMedia.url}`}
                controls
                className="max-w-full max-h-full"
                autoPlay
              />
            )}
          </div>
          
          <button
            onClick={() => setSelectedMedia(null)}
            className="absolute top-4 right-4 text-white text-2xl hover:text-gray-300"
          >
            ×
          </button>
        </div>
      )}
    </>
  );
};

export default MediaGallery;