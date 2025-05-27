import SignInput from "../components/SignInput/SignInput";
import SignButton from "../components/SignButton/SignButton";


export default function SignIn() {


    return (
        <>
            <SignInput ty="email">Email</SignInput>
            <SignInput ty="password">Password</SignInput>
            <SignInput ty="password">Confirm password</SignInput>
        </>
    );
}