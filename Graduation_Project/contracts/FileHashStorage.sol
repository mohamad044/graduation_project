// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

contract FileHashStorage {
    mapping(string => bool) private fileHashes;

    function storeHash(string memory _hash) public {
        fileHashes[_hash] = true;
    }

    function checkHash(string memory _hash) public view returns (bool) {
        return fileHashes[_hash];
    }
}
