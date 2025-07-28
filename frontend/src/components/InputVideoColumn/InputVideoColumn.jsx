import classes from "./InputVideoColumn.module.css";
import React, { useState, useEffect } from 'react';
import cameraPlaceholder from "../../img/SecurityCameraPNGImage.png";

const InputVideoColumn = (props) => {
    const [mediaUrl, setMediaUrl] = useState(null);
    const [isImage, setIsImage] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (mediaUrl) {
            URL.revokeObjectURL(mediaUrl);
        }

        const url = URL.createObjectURL(file);
        setMediaUrl(url);
        setIsImage(file.type.startsWith("image/")); // detect image

        props.onVideoUploaded(file);
    };

    return (
        <div className={classes.InputVideoColumn}>
            {!mediaUrl && (
                <div style={{
                    height: "80%",
                    width: "100%",
                    borderStyle: "solid",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column"
                }}>
                    <img src={cameraPlaceholder} style={{ width: "50%" }} alt="placeholder" />
                </div>
            )}

            {mediaUrl && !isImage && (
                <video width="100%" height="80%" style={{ objectFit: 'cover' }} src={mediaUrl} controls>
                    <source type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            )}

            {mediaUrl && isImage && (
                <img src={mediaUrl} width="100%" height="80%" style={{ objectFit: 'cover' }} alt="Uploaded" />
            )}

            <div style={{ height: "5%" }}></div>

            <label className={classes.ChooseVideoButton}>
                {/* Accept both video and image formats */}
                <input
                    type="file"
                    accept="video/*,image/*"
                    onChange={handleFileChange}
                />
                Choose file
            </label>
        </div>
    );
};

export default InputVideoColumn;
