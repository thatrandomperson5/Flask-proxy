self.addEventListener( "install", function( event ){
    self.skipWaiting();
});
self.addEventListener( "activate", event => {
    console.log('WORKER: activate event in progress.');
});
