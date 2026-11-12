
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();

const port = process.env.PORT || 3030;
const mongoUri = process.env.MONGODB_URI || "mongodb://mongo_db:27017/";

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const reviews_data = JSON.parse(
  fs.readFileSync(path.join(__dirname, "reviews.json"), "utf8")
);

const dealerships_data = JSON.parse(
  fs.readFileSync(path.join(__dirname, "dealerships.json"), "utf8")
);

const Reviews = require('./review');
const Dealerships = require('./dealership');

async function initializeDatabase() {
  await mongoose.connect(mongoUri, {
    dbName: 'dealershipsDB'
  });

  console.log("MongoDB connected successfully");

  const dealerCount = await Dealerships.countDocuments();

  if (dealerCount === 0) {
    await Dealerships.insertMany(dealerships_data.dealerships);
    console.log("Dealership sample data initialized");
  }

  const reviewCount = await Reviews.countDocuments();

  if (reviewCount === 0) {
    await Reviews.insertMany(reviews_data.reviews);
    console.log("Review sample data initialized");
  }
}



// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
//Write your code here
   try {
        const dealerships = await Dealerships.find();
        res.json(dealerships);
    } catch (error) {
        res.status(500).json({
            error: 'Error fetching dealerships'
        });
    }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
//Write your code here
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
//Write your code here
try {
        const dealerId = Number(req.params.id);

        if (!Number.isInteger(dealerId) || dealerId <= 0) {
            return res.status(400).json({
                error: 'Invalid dealer ID'
            });
        }

        const dealer = await Dealerships.findOne({
            id: dealerId
        });

        if (!dealer) {
            return res.status(404).json({
                error: 'Dealer not found'
            });
        }

        res.json(dealer);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: 'Error fetching dealer'
        });
    }
});

//Express route to insert review

app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = Buffer.isBuffer(req.body)
      ? JSON.parse(req.body.toString('utf8'))
      : typeof req.body === 'string'
        ? JSON.parse(req.body)
        : req.body;

    if (!data || !data.name || !data.dealership || !data.review) {
      return res.status(400).json({
        error: 'Missing required review information'
      });
    }

    const latestReview = await Reviews.findOne()
      .sort({ id: -1 });

    const newId = latestReview ? latestReview.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: Number(data.dealership),
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: Number(data.car_year)
    });

    const savedReview = await review.save();

    return res.status(201).json(savedReview);

  } catch (error) {
    console.error('Error inserting review:', error);

    return res.status(500).json({
      error: 'Error inserting review',
      details: error.message
    });
  }
});
// Start the Express server

async function startServer() {
  try {
    await initializeDatabase();

    app.listen(port, '0.0.0.0', () => {
      console.log(`Express API listening on port ${port}`);
    });
  } catch (error) {
    console.error("Failed to start Express API:", error);
    process.exit(1);
  }
}

startServer();

