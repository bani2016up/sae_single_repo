import { useState } from "react";
import { Link, Route, useNavigate } from "react-router-dom"; // <-- import useNavigate

import { API } from "../../constants";

import SignInput from "../SignInput/SignInput";
import SignButton from "../SignButton/SignButton";

import "./SignWrapper.css";

export default function SignWrapper({ children, htype }) {
    const navigate = useNavigate();

    if (children === 'Sign up') {
        const [email, setEmail] = useState('');
        const [password, setPassword] = useState('');
        const [confirm, setConfirm] = useState('');
        const [error, setError] = useState('');

        function handleSignUpButtonClick() {
            setError("");

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
                    .then(res => {
                        console.log('Status:', res.status);
                        console.log('Is ok:', res.ok);
                        console.log('Status:', res.statusText);
                        if (res.status === 200) {
                            navigate('/signin');
                        }
                        return res.json();
                    })
                    .then(data => {
                        console.log('Server response:', data);
                    })
                    .catch(error => {
                        setError('Failed to sign up.');
                        console.error('Error:', error);
                    });
                
            }
        }

        return (
            <div className="sign-wrapper">
                <img src="../src/assets/sae-logo.svg" alt="SAE" />
                <div className="wrapper">
                    {error && <span className="error-message">{error}</span>}
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
                    <span className="span-wrapper">Already have an account?</span>
                    <Link className="a-wrapper" to={'/sign' + htype}>{'Sign ' + htype}</Link>
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
                console.log("Sign in in process...");
                fetch(API + 'auth/sessions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                })
                    .then(res => {
                        console.log('Status:', res.status);
                        console.log('Is ok:', res.ok);
                        if (res.status === 200)
                            {
                                navigate('/editor')
                            }
                        return res.json();
                    })
                    .then(data => {
                        console.log('Server response:', data);
                    })
                    .catch(error => {
                        setError('Failed to sign in.');
                        console.error('Error:', error);
                    });
            }
        }

        return (
            <div className="sign-wrapper">
                <img className="img-wrapper" src="../src/assets/sae-logo.svg" alt="SAE" />
                <div className="wrapper">
                    {error && <span className="error-message">{error}</span>}
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
                    <span className="span-wrapper">Do not have an account?</span>
                    <Link className="a-wrapper" to={'/sign' + htype}>{'Sign ' + htype}</Link>
                </div>
            </div>
        );
    }
}
