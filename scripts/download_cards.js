const puppeteer = require('puppeteer');

async function downloadAllCards() {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    console.log('Opening page...');
    await page.goto('https://sites.google.com/view/noge-pokemontcgpocket-zh/%E5%8D%A1%E7%89%8C%E5%9C%96%E9%91%92', {
        waitUntil: 'networkidle2',
        timeout: 60000
    });
    
    // Wait for initial load
    await page.waitForTimeout(3000);
    
    // Scroll to load all cards
    console.log('Scrolling to load all cards...');
    let previousHeight = 0;
    let sameCount = 0;
    
    while (sameCount < 5) {
        const height = await page.evaluate(() => document.body.scrollHeight);
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(2000);
        
        if (height === previousHeight) {
            sameCount++;
        } else {
            sameCount = 0;
        }
        previousHeight = height;
        console.log(`Scrolled to ${height}px...`);
    }
    
    // Get all card data
    console.log('Extracting card data...');
    const cards = await page.evaluate(() => {
        const cardElements = document.querySelectorAll('.card img');
        return Array.from(cardElements).map(img => ({
            name: img.alt || 'unknown',
            img_id: img.dataset.src ? img.dataset.src.match(/\/d\/([^\/]+)/)[1] : null,
            src: img.src || img.dataset.src
        })).filter(c => c.img_id);
    });
    
    console.log(`Found ${cards.length} cards`);
    
    // Save card list
    const fs = require('fs');
    fs.writeFileSync('/home/node/.openclaw/workspace-celesteela/cards.json', JSON.stringify(cards, null, 2));
    console.log('Card list saved to cards.json');
    
    await browser.close();
    return cards;
}

downloadAllCards().catch(console.error);
