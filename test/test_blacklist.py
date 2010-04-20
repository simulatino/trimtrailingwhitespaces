from ttws import blacklisted

def test_blacklist():
	assert blacklisted(".git") == True
	assert blacklisted(".gi") == False
	assert blacklisted("git") == False
	assert blacklisted("foo/.svn/bar") == True
	assert blacklisted("foo/svn/bar") == False
	assert blacklisted("foo./svn/bar") == False
	assert blacklisted("foo/.cvs/bar") == True
	assert blacklisted("foo/cvs/bar") == False
	assert blacklisted("foo./cvs/bar") == False
	assert blacklisted("foo/.hg/bar") == True
	assert blacklisted("foo/hg/bar") == False
	assert blacklisted("foo./hg/bar") == False
	assert blacklisted("foo/.bzr/bar") == True
	assert blacklisted("foo/bzr/bar") == False
	assert blacklisted("foo./bzr/bar") == False
