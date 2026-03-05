import React, { useState, useEffect } from 'react';
import { Container, Form, Button, Card, Alert, Spinner } from 'react-bootstrap';
import { auth } from '../firebase';

const Report = () => {
  const [location, setLocation] = useState('');
  const [crowdLevel, setCrowdLevel] = useState('');
  const [notes, setNotes] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(null);
  const [locations, setLocations] = useState([])

  useEffect(() => {
          const fetchCrowds = () => {
              fetch('api/crowds')
                  .then(res => res.json())
                  .then(data => {
                      setLocations(data)
                      console.log("Crowd Levels:", data)
                  })
          }
  
          fetchCrowds(); 
  
          const intervalId = setInterval(fetchCrowds, 10000);
  
          return () => clearInterval(intervalId);
      }, [])

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log(location + " " + crowdLevel);
    // Simple validation: location and crowd level are required
    if (!location || !crowdLevel) {
      setError('Please fill in all required fields.');
      return;
    }
    
    const user = auth.currentUser;

    if (user) {
      const reportData = {
        user_id: auth.currentUser.uid,
        location,
        crowd_level: crowdLevel,
        // notes,
      };

      console.log("Report Data", reportData)

      fetch('api/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reportData)
      })
        .then(res => {
          if (!res.ok) {
            throw new Error('Failed to submit report');
          }
          return res.json();
        })
        .then(data => {
          console.log('Report submitted:', data);
          setSubmitted(true);
          setError(null);
        })
        .catch(err => {
          console.error('Error submitting report:', err);
          setError('Submission failed. Please try again later.');
        });
    } else {
      console.log("User not signed in, but report visible")
    }

    // Allow reporting again after 3 seconds
    setTimeout(() => {
      setSubmitted(false);
      setLocation('');
      setCrowdLevel('');
      setNotes('');
    }, 3000);
  };

  return (
    <Container className="mt-4">
      <Card className="shadow-sm p-4">
        <Card.Title>Report a Location</Card.Title>
        {submitted ? (
          <Alert variant="success">Thank you for your report!</Alert>
        ) : (
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formLocation">
              <Form.Label>Location</Form.Label>
              {locations === null ? <Spinner animation="border" /> :
                <Form.Select
                onChange={(e) => setLocation((e.target.value))}
                >
                {locations.map((location, index) => {
                    return (
                    <option key={index} > {location.name} </option>
                    );
                })}
                </Form.Select>
              }

            </Form.Group>

            <Form.Group className="mb-3" controlId="formCrowdLevel">
              <Form.Label>Crowd Level: {crowdLevel}</Form.Label>
                <Form.Range
                  className="crowd-slider"
                  min={0}
                  max={10}
                  step={1}
                  value={crowdLevel}
                  onChange={(e) => setCrowdLevel(Number(e.target.value))}
                  style={{
                    background: `linear-gradient(to right, ${
                      crowdLevel < 4 ? '#28a745' : crowdLevel < 7 ? '#ffc107' : '#dc3545'
                    } 0%, ${
                      crowdLevel * 10
                    }%, #dee2e6 ${crowdLevel * 10}%, #dee2e6 100%)`
                  }}
                />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formNotes">
              <Form.Label>Additional Notes (optional)</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="Enter any additional details"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </Form.Group>

            {error && <Alert variant="danger">{error}</Alert>}

            <Button variant="primary" type="submit">
              Submit Report
            </Button>
          </Form>
        )}
      </Card>
    </Container>
  );
};

export default Report;
