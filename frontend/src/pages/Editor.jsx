



export default function Editor() {
    return (
        <div className="editor">
            <h1>Editor Page</h1>
            <p>This is the editor page where you can create and edit content.</p>
            <textarea placeholder="Start writing your content here..." rows="10" cols="50"></textarea>
            <br />
            <button type="submit">Save</button>
        </div>
        
    );
}