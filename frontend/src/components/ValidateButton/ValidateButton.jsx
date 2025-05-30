import "./ValidateButton.css";


export default function ValidateButton({ onClick, disabled }) {
    return (
        <button
            className="validate-button"
            onClick={onClick}
            disabled={disabled}
        >
            Validate
        </button>
    );
}