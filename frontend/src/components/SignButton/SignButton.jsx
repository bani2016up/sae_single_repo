import "./SignButton.css";


export default function SignButton({ children }) {
    function handleClick() {
        console.log("SingButton button clicked");
    }

    return (<button className="sign-button" onClick={handleClick}>
        {children}
    </button>
    )

}

