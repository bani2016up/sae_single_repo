// Example: TextArea.jsx
import "./TextArea.css";
import { useRef } from "react";

export default function TextArea({ value, onChange }) {
    const ref = useRef();

    function autoResize(e) {
        ref.current.style.height = "auto";
        ref.current.style.height = ref.current.scrollHeight + "px";
        if (onChange) onChange(e); // Call parent onChange if provided
    }

    return (
        <textarea
            className="text-area"
            ref={ref}
            value={value}
            onInput={autoResize}
            onChange={onChange}
        />
    );
}