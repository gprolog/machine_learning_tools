var Hzip = require( './third_party/hzip/hzip' );
var inflate = require( './third_party/deflate-js/rawinflate' );
var fs = require( 'fs' );

var JarFile = function( filepath ) {
	this.filepath_ = filepath;
	this.hzip_ = null;
}

JarFile.prototype.getEntryData = function( entryName ) {
    try {
        if ( !this.hzip_ ) this.hzip_ = new Hzip( fs.readFileSync( this.filepath_ ) );

        var entry = this.hzip_.getEntry( entryName );
        var entryData = null;

        return inflate( entry.cfile );

    } catch ( ex ) {
        console.log( ex );
    }
	

    

}



module.exports = JarFile;