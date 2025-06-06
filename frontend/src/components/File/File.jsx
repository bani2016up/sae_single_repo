import fileIcon from '../../assets/file-text.svg';
import "./File.css";

export default function File({ name, handleClick }) {
    return (
        <button className="file-selector" onClick={handleClick}>
            <img className="img-selector" src={fileIcon} alt="File icon" />
            <span className="span-selector">{name}</span>
        </button>
    );
}