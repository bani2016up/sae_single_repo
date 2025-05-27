// import React from 'react';
import './SignInput.css';

export default function SignInput({ children, ty }) {

    return (
        <div className="sign-input">
            <input type={ty} placeholder={children} />
        </div>
    )
}