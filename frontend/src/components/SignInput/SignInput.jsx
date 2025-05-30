// import React from 'react';
import './SignInput.css';

export default function SignInput({ children, ty, min_len, max_len, value, onChange}) {
    return (
        <div className="sign-input">
            <input className="input-sign"
                minLength={min_len}
                maxLength={max_len}
                type={ty}
                placeholder={children}
                value={value}
                onChange={onChange}
            />
        </div>
    );
}