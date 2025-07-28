import classes from "./ProcessedVideoColumn.module.css";
import React, { useState, useEffect } from 'react';
import outputPlaceholder from "../../img/output.png";

const ProcessedVideoColumn = ({ processedMedia }) => {
    const [mediaUrl, setMediaUrl] = useState(null);
    const [isImage, setIsImage] = useState(false);

    useEffect(() => {
        if (processedMedia) {
            const url = URL.createObjectURL(processedMedia);
            setMediaUrl(url);
            setIsImage(processedMedia.type.startsWith("image/"));
        }
    }, [processedMedia]);

    return (
        <div className={classes.ProcessedVideoColumn}>
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
                    <img src={outputPlaceholder} style={{ width: "50%" }} alt="placeholder" />
                </div>
            )}

            {mediaUrl && !isImage && (
                <video width="100%" height="80%" style={{ objectFit: 'cover' }} src={mediaUrl} controls>
                    <source type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            )}

            {mediaUrl && isImage && (
                <img src={mediaUrl} width="100%" height="80%" style={{ objectFit: 'cover' }} alt="Processed" />
            )}
        </div>
    );
};

export default ProcessedVideoColumn;
