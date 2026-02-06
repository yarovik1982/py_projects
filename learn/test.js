const symbols = {
   msg: "Привет Паша",
   slash: "\\",
   pipe: "|",
   hat: "^",
   space: " ",
   o: "o",
   dash: "-",
   eq: "=",
};

// function cowsay(msg) {
   const top = " " + "_".repeat(symbols.msg.length + 2);
   const middle = `| ${symbols.msg} |`;
   const bottom = " " + symbols.eq.repeat(symbols.msg.length + 2);

   const cow = `
            
             ^__^
             (${symbols.o}${symbols.o})\\_______
             (__)\\       )\\/\\
              ${symbols.space}  ||---${symbols.dash}w${symbols.pipe}${symbols.pipe}
                 ||     ||
    `;

   console.log(top);
   console.log(middle);
   console.log(bottom);
   console.log(cow);
// }

// cowsay(symbols.msg);

// function printCow() {
//    const arrTop = top.split(" ");
//    for (let i = 0; i < arrTop.length; i++) {
//       setTimeout(() => {
//          console.log(arrTop[i]);
//       },300 * i)
//    }
//    // console.log(arrTop);
// }
// printCow();
