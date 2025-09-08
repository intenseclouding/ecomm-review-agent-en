import React, { useState, useRef } from 'react';

interface MediaFile {
  file: File;
  preview: string;
  type: 'image' | 'video';
}

interface MediaUploadProps {
  onFilesChange: (files: File[]) => void;
  maxFiles?: number;
}

const MediaUpload: React.FC<MediaUploadProps> = ({ onFilesChange, maxFiles = 5 }) => {
  const [mediaFiles, setMediaFiles] = useState<MediaFile[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const validFiles = files.filter(file => {
      const isImage = file.type.startsWith('image/');
      const isVideo = file.type.startsWith('video/');
      const isValidSize = file.size <= 50 * 1024 * 1024; // 50MB limit
      return (isImage || isVideo) && isValidSize;
    });

    if (mediaFiles.length + validFiles.length > maxFiles) {
      alert(`최대 ${maxFiles}개의 파일만 업로드할 수 있습니다.`);
      return;
    }

    const newMediaFiles = validFiles.map(file => ({
      file,
      preview: URL.createObjectURL(file),
      type: file.type.startsWith('image/') ? 'image' as const : 'video' as const
    }));

    const updatedFiles = [...mediaFiles, ...newMediaFiles];
    setMediaFiles(updatedFiles);
    onFilesChange(updatedFiles.map(mf => mf.file));
  };

  const removeFile = (index: number) => {
    URL.revokeObjectURL(mediaFiles[index].preview);
    const updatedFiles = mediaFiles.filter((_, i) => i !== index);
    setMediaFiles(updatedFiles);
    onFilesChange(updatedFiles.map(mf => mf.file));
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        사진 및 동영상 ({mediaFiles.length}/{maxFiles})
      </label>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-gray-400 transition-colors">
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*,video/*"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={mediaFiles.length >= maxFiles}
          className="text-blue-500 hover:text-blue-600 disabled:text-gray-400"
        >
          📷 사진/동영상 추가
        </button>
        
        <p className="text-xs text-gray-500 mt-1">
          이미지, 동영상 파일 (최대 50MB, {maxFiles}개까지)
        </p>
      </div>

      {mediaFiles.length > 0 && (
        <div className="mt-4 grid grid-cols-2 gap-2">
          {mediaFiles.map((media, index) => (
            <div key={index} className="relative group">
              {media.type === 'image' ? (
                <img
                  src={media.preview}
                  alt={`Preview ${index + 1}`}
                  className="w-full h-24 object-cover rounded-lg"
                />
              ) : (
                <video
                  src={media.preview}
                  className="w-full h-24 object-cover rounded-lg"
                  controls={false}
                />
              )}
              
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity"
              >
                ×
              </button>
              
              <div className="absolute bottom-1 left-1 bg-black bg-opacity-50 text-white text-xs px-1 rounded">
                {media.type === 'video' ? '🎥' : '📷'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MediaUpload;