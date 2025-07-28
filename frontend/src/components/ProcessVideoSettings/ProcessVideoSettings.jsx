import classes from "./ProcessVideoSettings.module.css";
import { useState, useEffect } from "react";
import { HOST } from "../../api/config";

const ProcessVideoSettings = ({ uploadedVideo, onVideoProcessed }) => {
    const [mode, setMode] = useState("");
    const [fps, setFps] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);

    const isFormValid = uploadedVideo && mode && fps;

    useEffect(() => {
        const processButton = document.getElementById("processButton");
        if (processButton) {
            processButton.disabled = !isFormValid;
        }
    }, [uploadedVideo, mode, fps]);

    const handleModeChange = (e) => setMode(e.target.value);
    const handleFpsChange = (e) => setFps(parseInt(e.target.value, 10));

    const requestVideoProcess = async () => {
        try {
            if (!isFormValid) {
                alert("Please select mode, FPS, and upload a video.");
                return;
            }

            const formData = new FormData();
            formData.append("file", uploadedVideo);
            formData.append("mode", mode);
            formData.append("fps", fps);

            setIsProcessing(true);
            const url = `http://${HOST}:8000/upload`;

            const response = await fetch(url, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Server returned status ${response.status}`);
            }

            const videoData = await response.arrayBuffer();
            const videoBlob = new Blob([videoData], { type: "video/mp4" });
            const videoFile = new File([videoBlob], uploadedVideo.name, { type: "video/mp4" });

            onVideoProcessed(videoFile);
        } catch (error) {
            console.error("Error during video processing:", error);
            alert("Video processing failed. Please check the console for details.");
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className={classes.ProcessVideoSettings}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <label style={{ fontSize: 32, fontFamily: "Inter" }}>Mode</label>
                <select
                    id="ModeSelect"
                    value={mode}
                    onChange={handleModeChange}
                    style={{ padding: "5%", width: "180px", height: "48px", fontSize: "18px" }}
                >
                    <option value="">Select</option>
                    <option value="Fragmentation">FRAG (Just fragmentation)</option>
                    <option value="Segmentation">SEG (Segmentation)</option>
                    <option value="HPE">HPE (Human pose estimation)</option>
                    <option value="HPE, SEG">HPE + SEG</option>
                    <option value="Detection">DET (Detection)</option>
                </select>
            </div>

            <div style={{ height: "10%" }}></div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <label style={{ fontSize: 32, fontFamily: "Inter" }}>FPS</label>
                <select
                    id="fpsSelect"
                    value={fps}
                    onChange={handleFpsChange}
                    style={{ padding: "5%", width: "100px", height: "48px", fontSize: "18px" }}
                >
                    <option value="">Select</option>
                    {[1, 2, 4, 8, 16, 32].map((val) => (
                        <option key={val} value={val}>
                            {val}
                        </option>
                    ))}
                </select>
            </div>

            <div style={{ height: "10%" }}></div>

            <button
                id="processButton"
                className={classes.ProcessVideoButton}
                onClick={requestVideoProcess}
                disabled={!isFormValid || isProcessing}
            >
                {isProcessing ? "Processing..." : "Process"}
            </button>
        </div>
    );
};

export default ProcessVideoSettings;
