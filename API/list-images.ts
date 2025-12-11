import { VercelRequest, VercelResponse } from '@vercel/node';
import * as fs from 'fs';
import * as path from 'path';

// Allowed image extensions
const ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'];

// Vercel Serverless Function Handler
export default function (req: VercelRequest, res: VercelResponse) {
    try {
        // Vercel puts the deployment bundle in the current working directory.
        // We need to navigate to the correct static asset folder:
        // Current directory is the Serverless Function's execution context.
        const IMAGE_DIR = path.join(process.cwd(), 'public', 'images');

        if (!fs.existsSync(IMAGE_DIR)) {
            // Log an error if the directory isn't found
            console.error(`Image directory not found at: ${IMAGE_DIR}`);
            return res.status(500).json({ error: 'Server configuration error: Image directory missing.' });
        }

        // Read all files in the directory
        const allFiles = fs.readdirSync(IMAGE_DIR);
        
        // Filter for allowed image files
        const imageList = allFiles.filter(fileName => {
            const ext = path.extname(fileName).toLowerCase();
            return ALLOWED_EXTENSIONS.includes(ext);
        });

        // Return the JSON list
        return res.status(200).json(imageList);

    } catch (e) {
        console.error('API Error:', e);
        // Cast 'e' to Error to access the message property
        return res.status(500).json({ error: (e as Error).message || 'Internal Server Error' });
    }
}
