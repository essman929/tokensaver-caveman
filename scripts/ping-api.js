#!/usr/bin/env node

'use strict';

const https = require('https');
const http = require('http');

const API_URL = process.env.PING_URL || 'https://httpbin.org/get';
const INTERVAL_MS = parseInt(process.env.PING_INTERVAL_MS || '5000', 10);

function ping(url) {
  const start = Date.now();
  const client = url.startsWith('https') ? https : http;

  const req = client.get(url, (res) => {
    res.resume();
    res.on('end', () => {
      const ms = Date.now() - start;
      console.log(`[${new Date().toISOString()}] ${url} → ${res.statusCode} (${ms}ms)`);
    });
  });

  req.on('error', (err) => {
    const ms = Date.now() - start;
    console.error(`[${new Date().toISOString()}] ${url} → ERROR (${ms}ms): ${err.message}`);
  });

  req.setTimeout(10000, () => {
    req.destroy(new Error('Request timed out'));
  });
}

console.log(`Pinging ${API_URL} every ${INTERVAL_MS}ms. Ctrl+C to stop.`);
ping(API_URL);
setInterval(() => ping(API_URL), INTERVAL_MS);
