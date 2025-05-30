import "./SignButton.css";


export default function SignButton({ children, handleSignButtonClick_ }) {

    return (
        <button
            className="sign-button"
            onClick={handleSignButtonClick_} 
        >
            {children}
        </button>
    )

}

