from link import BaseLink
import library.symboltable

class FullLink(BaseLink):
    symboltable = library.symboltable.buildsymboltable()

    def sendto(self, target):
        """Packs the link into a carrier designed to bring it somewhere fast, and returns the combination of that with the target."""
        runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar".split())
        rev_runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar"[::-1].split())
        # Prepare the packet
        carrier = BaseLink(runes[self.link, ("Rit", "Vor", "Dorn")])
        # Send
        target += carrier
        # Unpack packet
        target = BaseLink(rev_runes[target.link, ("nroD", "roV", "tiR")])
        return target

    def freeze(self):
        """Packs the current link with very static and heavy runes designed to keep it together and in one place."""
        runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar".split())
        self.link = runes[self.link, ("Is", "Jera", "Ka")]
