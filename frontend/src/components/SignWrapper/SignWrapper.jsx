import { useState } from "react";
import { Link } from "react-router-dom";

import { API } from "../../constants";

import SignInput from "../SignInput/SignInput";
import SignButton from "../SignButton/SignButton";

import "./SignWrapper.css";

export default function SignWrapper({ children, htype}) {

    if (children === 'Sign up') {
        const [email, setEmail] = useState('');
        const [password, setPassword] = useState('');
        const [confirm, setConfirm] = useState('');
        const [error, setError] = useState(''); // <-- Add error state

        function handleSignUpButtonClick() {
            setError(""); // Clear previous error

            if (email === "" || password === "" || confirm === "") {
                console.error("Empty field error");
                setError("Please fill in all fields.");
                return;
            } else if (password.length < 8 || password.length > 64) {
                console.error("Password length error");
                setError("Password length must be more than 8");
                return;
            } else if (password !== confirm) {
                console.error("Password mismatch error");
                setError("Passwords do not match.");
                return;
            } else {
                setError(""); // No error
                console.log("Sign up in process...");
                fetch(API + 'auth/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                })
                    .then(res => res.json())
                    .then(data => {
                        console.log('Server response:', data);
                        // handle server response (e.g., show success, redirect, etc.)
                    })
                    .catch(error => {
                        setError('Failed to sign up.');
                        console.error('Error:', error);
                    });
            }
        }

        return (
            <div className="sign-wrapper">
                <img src="../src/assets/SAE logo.svg" alt="SAE" />
                <div className="wrapper">
                    {error && <text className="error-message">{error}</text>}
                    <SignInput
                        ty="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    >Email</SignInput>
                    <SignInput
                        max_len={64}
                        min_len={8}
                        ty="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    >Password</SignInput>
                    <SignInput
                        max_len={64}
                        min_len={8}
                        ty="password"
                        value={confirm}
                        onChange={e => setConfirm(e.target.value)}
                    >Confirm Password</SignInput>
                    <SignButton handleSignButtonClick_={handleSignUpButtonClick}>{children}</SignButton>
                </div>
                <div className="sign-text">
                    <text>Already have an account?</text>
                    <Link to={'/sign' + htype}>{'Sign ' + htype}</Link>
                </div>
            </div>
        );
    }
    else if (children === 'Sign in') {
        const [email, setEmail] = useState('');
        const [password, setPassword] = useState('');
        const [error, setError] = useState(''); // <-- Add error state

        function handleSignInButtonClick() {
            setError(""); // Clear previous error

            if (email === "" || password === "" || confirm === "") {
                console.error("Empty field error");
                setError("Please fill in all fields.");
                return;
            } else if (password.length < 8 || password.length > 64) {
                console.error("Password length error");
                setError("Password length must be more than 8");
                return;
            } else {
                setError(""); // No error
                console.log("Sign up in process...");
                fetch(API + 'auth/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                })
                    .then(res => res.json())
                    .then(data => {
                        console.log('Server response:', data);
                        // handle server response (e.g., show success, redirect, etc.)
                    })
                    .catch(error => {
                        setError('Failed to sign up.');
                        console.error('Error:', error);
                    });
            }
        }

        return (
            <div className="sign-wrapper">
                <img src="../src/assets/SAE logo.svg" alt="SAE" />
                <div className="wrapper">
                    {error && <text className="error-message">{error}</text>}
                    <SignInput
                        ty="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    >Email</SignInput>
                    <SignInput
                        max_len={64}
                        min_len={8}
                        ty="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    >Password</SignInput>
                    <SignButton handleSignButtonClick_={handleSignInButtonClick}>{children}</SignButton>
                </div>
                <div className="sign-text">
                    <text>Do not have an account?</text>
                    <Link to={'/sign' + htype}>{'Sign ' + htype}</Link>
                </div>
            </div>
        );
    }
}
