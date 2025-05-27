import { Children } from "react";

import SignInput from "../SignInput/SignInput";
import SignButton from "../SignButton/SignButton";

import "./SignWrapper.css";

export default function SignWrapper({ children}) {

    if (children == "Sign up") {
        return (
            <div className="sign-wrapper">
                <img src="../src/assets/SAE logo.svg" alt="SAE" />
                <div className="wrapper">
                    <SignInput ty="email">Email</SignInput>
                    <SignInput ty="password">Password</SignInput>
                    <SignInput ty="password">Confirm password</SignInput>
                    <SignButton>{ children }</SignButton>
                </div>
                    <div className="sign-text">
                        Already have an account?
                        <a href="#">Sing in</a>
                    </div>
            </div>
        );
    }
    else if (children == "Sign in")
    {
        
    }

}